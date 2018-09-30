$(function () {
    var simplemde = new SimpleMDE({
        showIcons: ["code", "table"],
        renderingConfig: {
            codeSyntaxHighlighting: true
        },
        spellChecker: false
    });
    $('#tags').multiselect();
    $('#category').multiselect();
});
