<template>
    <div class="markdown-editor">
        <div class="markdown-editor-toolbar" style="display: inline-block;">
            <div>
                <a href="#" class="nav-link">
                    <span class="oi oi-bold"></span>
                </a>
            </div>
            <div>
                <a href="#" class="nav-link">
                    <span class="oi oi-italic"></span>
                </a>
            </div>
        </div>
        <div class="markdown-editor-main" ref="editorMain">
            <textarea ref="editorTextArea" v-model="rawValue"></textarea>
            <div class="preview" :style="{width: editorPreviewWidth + 'px'}" v-html="compiledHtml"></div>
        </div>
    </div>
</template>


<script>
    import marked from "marked";

    export default {
        data() {
            return {
                editorPreviewWidth: null,
                rawValue: "",
            }
        },

        mounted() {
            let editorMain = this.$refs.editorMain;
            let editorTextArea = this.$refs.editorTextArea;

            let editorMainWidth = editorMain.clientWidth;
            let editorMainHeight = editorMain.clientHeight;

            let editorTextAreaWidth = editorTextArea.clientWidth;
            let editorTextAreaHeight = editorTextArea.clientHeight;

            this.editorPreviewWidth = editorMainWidth - editorTextAreaWidth;


            let MutationObserver = window.MutationObserver || window.WebKitMutationObserver || window.MozMutationObserver;
            this.observer = new MutationObserver((mutationList) => {
                for (let mutation of mutationList) {
                    let width = parseInt(editorTextArea.clientWidth);
                    let height = parseInt(editorTextArea.style.height);
                    this.editorPreviewWidth = editorMainWidth - width;
                }
            });

            this.observer.observe(editorTextArea, {
                attributes: true,
                attributeFilter: ["style"],
                attributeOldValue: true
            });
        },

        computed: {
            compiledHtml() {
                return marked(this.rawValue);
            }
        },

        created() {
        },

        beforeDestroy() {
            if (this.observer) {
                this.observer.disconnect();
                this.observer.takeRecords();
                this.observer = null;
            }
        }
    }

</script>


<style lang="stylus" scoped>
    .markdown-editor {
        border: 1px solid #ccc;
        border-radius: 4px;

        .markdown-editor-toolbar {
            border-bottom: none;
            height: 40px;
        }

        .markdown-editor-main {
            height: 600px;
            display: flex;
            flex-flow: row nowrap;
            justify-content: space-between;
            align-items: stretch;

            textarea {
                margin: 0
                padding-left: 10px;
                padding-right: 10px;
                outline: none;
                width: 50%;
                resize: none;
                border-top: 1px solid #ccc;
                border-right: 1px solid #ccc;
                border-left: none;
                border-bottom: none;
                box-sizing: border-box;
            }

            .preview {
                margin: 0
                padding-left: 10px;
                padding-right: 10px;
                background-color: #f6f6f6;
                border-top: 1px solid #ccc;
                border-left: none;
                border-bottom: none;
                box-sizing: border-box;
            }
        }
    }
</style>