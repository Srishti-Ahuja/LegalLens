import hashlib
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import pdf_service, gemini_service, vector_service

logger = logging.getLogger(__name__)

class UploadView(APIView):
    def post(self, request):
        if 'file' not in request.FILES:
            return Response({'error': True, 'message': 'No file provided.'}, status=status.HTTP_400_BAD_REQUEST)
        
        file_obj = request.FILES['file']
        
        if not file_obj.name.lower().endswith('.pdf'):
            return Response({'error': True, 'message': 'Only PDF files are supported.', 'code': 'INVALID_FILE_TYPE'}, status=status.HTTP_400_BAD_REQUEST)
            
        if file_obj.size > 10 * 1024 * 1024:
            return Response({'error': True, 'message': 'File exceeds 10MB limit.', 'code': 'FILE_TOO_LARGE'}, status=status.HTTP_400_BAD_REQUEST)
            
        file_content = file_obj.read()
        file_hash = hashlib.sha256(file_content).hexdigest()
        
        try:
            # 1. Save Document record
            doc_id = vector_service.save_document(file_obj.name, file_hash)
            
            full_text = []
            
            import concurrent.futures

            # 2. Extract and Chunk
            chunks = list(pdf_service.extract_and_chunk_pdf(file_content, file_obj.name))
            
            def process_chunk(chunk_data):
                vector_service.save_chunk(
                    doc_id, 
                    chunk_data['page_number'], 
                    chunk_data['chunk_index'], 
                    chunk_data['content']
                )
                return chunk_data['content']

            full_text = []
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                full_text = list(executor.map(process_chunk, chunks))

            # Combine all chunk texts
            joined_text = " ".join(full_text).strip()

            if not joined_text:
                logger.warning("No extracted text from PDF; skipping analysis.")
                summary = "No document text could be extracted."
                risks = []
            else:
                # 3. Analyze using Gemini concurrently
                with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                    summary_future = executor.submit(gemini_service.generate_plain_summary, joined_text)
                    risks_future = executor.submit(gemini_service.extract_clause_risks, joined_text)
                    summary = summary_future.result()
                    risks = risks_future.result()
            
            vector_service.update_document_analysis(doc_id, summary, risks)
            
            return Response({
                'document_id': doc_id,
                'summary': summary,
                'risks': risks
            })
            
        except Exception as e:
            return Response({'error': True, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ChatView(APIView):
    def post(self, request):
        # Robust payload extraction: handle DRF JSON, form data, and raw body
        try:
            data = request.data if request.data else None
        except Exception:
            data = None
        if not data:
            if hasattr(request, 'POST') and request.POST:
                data = request.POST
            else:
                try:
                    import json
                    data = json.loads(request.body.decode('utf-8'))
                except Exception:
                    return Response({'error': True, 'message': 'Invalid JSON payload.'}, status=status.HTTP_400_BAD_REQUEST)

        query = data.get('query')
        document_id = data.get('document_id')
        if not query or not document_id:
            return Response({'error': True, 'message': 'Query and document_id required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            context_chunks = vector_service.search_similar_chunks(query, document_id)
            joined_context = " ".join(context_chunks).strip()
            if not joined_context:
                logger.warning("No context chunks found for document_id=%s; returning fallback answer.", document_id)
                answer = "I couldn't find any relevant content in the document to answer your question."
            else:
                try:
                    answer = gemini_service.answer_document_query(query, [joined_context])
                except Exception as gemini_err:
                    logger.exception("Gemini answer generation failed: %s", gemini_err)
                    answer = "I couldn't retrieve an answer at this time. Please try again later."
            return Response({'answer': answer})
        except Exception as e:
            logger.exception("ChatView processing failed: %s", e)
            fallback_msg = "Sorry, I encountered an error while answering your question."
            return Response({'answer': fallback_msg}, status=status.HTTP_200_OK)

class CompareView(APIView):
    def post(self, request):
        if 'file_a' not in request.FILES or 'file_b' not in request.FILES:
            return Response({'error': True, 'message': 'Two files required.'}, status=status.HTTP_400_BAD_REQUEST)
            
        # Simplified for brevity: extract full text directly. In production, consider chunking.
        try:
            import io
            from pypdf import PdfReader
            
            def extract_all(f) -> str:
                reader = PdfReader(io.BytesIO(f.read()))
                return " ".join([page.extract_text() or "" for page in reader.pages])
                
            text_a = extract_all(request.FILES['file_a'])
            text_b = extract_all(request.FILES['file_b'])
            
            diff_matrix = gemini_service.compare_contracts(text_a, text_b)
            return Response({'diff': diff_matrix})
            
        except Exception as e:
             return Response({'error': True, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
