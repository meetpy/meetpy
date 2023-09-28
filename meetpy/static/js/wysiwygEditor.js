"use strict";
window.onload = (event) => {
  const glob_theme = window.matchMedia?.("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  function initMdWysiwyg(textarea) {
    const theme = textarea.classList.contains("wysiwygEditor-allowDark")?glob_theme:"light";
    console.log(textarea.classList, theme);
    const Editor = toastui.Editor;
    const editorContainer = document.createElement("div");
    if (textarea.classList.contains("vLargeTextField")) {
      editorContainer.style.display = "inline-block";
    }
    textarea.after(editorContainer);
    textarea.style.display = "none";
    const editor = new Editor({
      el: editorContainer,
      height: 'auto',
      initialEditType: 'markdown',
      previewStyle: 'tab',
      usageStatistics: false,
      hideModeSwitch: true,
      previewHighlight: false,
      autofocus: false,
      theme: theme,
    });
    editor.setMarkdown(textarea.value)
    editor.on('blur', function () {
      textarea.value = editor.getMarkdown();
    })
  }

  function initWysiwygByQuery(query) {
    for (let el of document.querySelectorAll(query)) {
      initMdWysiwyg(el)
    }
  }

  initWysiwygByQuery("textarea.wysiwygEditor");
};
