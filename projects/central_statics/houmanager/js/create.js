//Front end communicating with the pyside2 manager
window.onload = function() {
    new QWebChannel(qt.webChannelTransport, function(channel) {
        window.manager = channel.objects.manager;
        const total_bundles = parseInt(JSON.parse(document.getElementById('total_bundles').textContent));

        for(let index=1; index<=total_bundles; ++index){
            let imports = document.getElementById(`import-file-${index}`);
            let videoImports = document.getElementById(`video-import-file-${index}`);
            imports.onclick = function (element) {
                manager.import_file(element.srcElement.dataset.filepath, element.srcElement.dataset.context,element.srcElement.dataset.bundlelist,element.srcElement.dataset.bundlename);
            }; 
            videoImports.onclick = function (element) {
                manager.import_file(element.srcElement.dataset.filepath, element.srcElement.dataset.context,element.srcElement.dataset.bundlelist,element.srcElement.dataset.bundlename);
            };
        } 
        
    });
}