/*
  Differ is a Python library class that outputs human readable differences.
  The below JS function creates a new DOM object and returns this.
  http://docs.python.org/library/difflib.html#difflib.Differ
*/

pydifferviewer = {
  as_tbody: function (params) {
    var differ_output = params.differ_output;

    tbody = document.createElement('tbody');

    function get_row(beforeline, afterline, data, classname) {
      tr = document.createElement('tr');
      $(tr).prop('class', classname)

      td1 = document.createElement('td');
      $(td1).prop('class', 'linenumber before');
      $(td1).append(document.createTextNode(beforeline))

      td2 = document.createElement('td');
      $(td2).prop('class', 'linenumber after');
      $(td2).append(document.createTextNode(afterline))

      td3 = document.createElement('td');
      $(td3).prop('class', 'data');
      $(td3).append(document.createTextNode(data))

      $(tr).append(td1, td2, td3);
      return tr
    }
    beforeline = 1;
    afterline = 1;
    last_operation = "equal";
    diff_found = false;
    for (var i=0; i < differ_output.length; i++) {
      change = differ_output[i];
      switch (change[0]) {
        case " ":
          if (last_operation=="insert" || last_operation == "delete") {
            // Equal
            $(tbody).append(
              get_row(
                beforeline++,
                afterline++,
                change,
                "equal"));
            last_operation = "equal";
          } else {
            beforeline++;
            afterline++;
          }
          break;
        case "+":
          // Insertion
          $(tbody).append(
            get_row(
              "",
              afterline++,
              change,
              "insert"));
          last_operation = "insert";
          break;
        case "-":
          // Deletion
          $(tbody).append(
            get_row(
              beforeline++,
              "",
              change,
              "delete"));
          last_operation = "delete";
          break;
        case "?":
          // Indicator of change
          break;
        default:
          alert("The first character of Differ output was not understood: " + change[0]);
          break;
      }
      if (last_operation != "equal") diff_found = true;
    }

    if (!diff_found) {
      $(tbody).append(get_row("-", "-", "(all data equal)", "equal"));
    }

    return tbody;

  }
}
