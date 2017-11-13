$.fn.extend({
    insertAtCaret: function(text){
        var editor = document.querySelector(".ace_editor").env.editor;
        var cursor = editor.selection.getCursor(); // returns object like {row:1 , column: 4}
        return editor.insert(text); // insert string at cursor
    },
    wrapSelection: function(openWrap, closeWrap){
        return this.each(function(i) {
            if (document.selection) {
            //For browsers like Internet Explorer
            this.focus();
            sel = document.selection.createRange();
            sel.text = openWrap + sel.text + closeWrap;
            this.focus();
            }
            else if (this.selectionStart || this.selectionStart == '0') {
            //For browsers like Firefox and Webkit based
            var startPos = this.selectionStart;
            var endPos = this.selectionEnd;
            var scrollTop = this.scrollTop;
            this.value = this.value.substring(0, startPos) + openWrap + this.value.substring(startPos,endPos) + closeWrap + this.value.substring(endPos,this.value.length);
            this.focus();
            this.selectionStart = startPos + openWrap.length;
            this.selectionEnd = endPos + openWrap.length;
            this.scrollTop = scrollTop;
            } else {
            this.value += openWrap + closeWrap;
            this.focus();
            }
        })
    }
});
