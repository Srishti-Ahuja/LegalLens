import React from 'react';

export default function Link({ children, href, className, ...props }: any) {
  return (
    <a href={href} className={className} {...props}>
      {children}
    </a>
  );
}
