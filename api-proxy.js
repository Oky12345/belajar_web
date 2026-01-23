<!-- Di index.html, pastikan urutan ini: -->
<head>
    <!-- ... -->
    <script src="https://cdn.jsdelivr.net/npm/axios@1.6.0/dist/axios.min.js"></script>
    <script src="api-proxy.js"></script>  <!-- ⭐ HARUS SEBELUM script.js -->
    <script src="script.js"></script>     <!-- ⭐ SETELAH api-proxy.js -->
</head>
