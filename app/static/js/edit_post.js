$(function () {
    var simplemde = new SimpleMDE({
        showIcons: ["code", "table"],
        renderingConfig: true
    });
    $('#tags').multiselect();
    $('#category').multiselect();
});
