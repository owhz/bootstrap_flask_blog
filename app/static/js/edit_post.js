$(function () {
    var simplemde = new SimpleMDE({
        autoDownloadFontAwesome: true,
        showIcons: ["code", "table", "strikethrough", "heading-smaller", 
            "heading-bigger", "unordered-list", "ordered-list",
            "clean-block", "horizontal-rule", ""],
        renderingConfig: {
            codeSyntaxHighlighting: true
        },
        spellChecker: false,
        tabSize: 4,
        indentWithTabs: false
    });
    $('#tags').multiselect();
    $('#category').multiselect();
});
