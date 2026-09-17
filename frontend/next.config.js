/** @type {import('next').NextConfig} */
const nextConfig = {
    // output: 'export', // removed for server mode

    images: {
        unoptimized: true,
    }
};

module.exports = nextConfig;
