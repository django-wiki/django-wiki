$.fn.extend({
    insertAtCaret: function(newValue){
        var cm = $('.CodeMirror')[0].CodeMirror;
        var doc = cm.getDoc();
        var cursor = doc.getCursor(); // gets the line number in the cursor position
        var line = doc.getLine(cursor.line); // get the line contents
        var pos = { // create a new object to avoid mutation of the original selection
            line: cursor.line,
            ch: line.length - 1 // set the character position to the end of the line
        };
        return doc.replaceRange(newValue, pos); // adds a new line
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
        });
    }
});
