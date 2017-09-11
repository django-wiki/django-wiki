$.ajaxSetup({
  beforeSend: function(xhr, settings) {
    if (settings.type == 'POST' && !this.crossDomain) {
      xhr.setRequestHeader("X-CSRFToken", jQuery("[name=csrfmiddlewaretoken]").val());
    }
  }
})


function wiki_input_post_data(url, val) {
  $.ajax({
    url: url,
    type: 'POST',
    data: JSON.stringify(val),
    contentType: "application/json",
    error: function(data){
      $('.notification-cnt').html("<b>!</b>");
    },
  });
}

function wiki_input_get_data(field, fn) {
  $.ajax({
    url: field.attr('data-url'),
    type: 'GET',
    contentType: "application/json",
    success: fn,
    error: function(data){
      $('.notification-cnt').html("<b>!</b>");
    },
  });
}


$(document).ready(function() {
  $('span[data-url][data-variant=all].dw-input').each(function() {
    var e = $(this);

    $.ajax({
      url: e.attr('data-url') + "?all",
      type: 'GET',
      contentType: "application/json",
      success: function(data, st, xhr) {
        if (xhr.status == 200) {
          if ($.templates['getAllTmpl']) {
            e.html($.render.getAllTmpl(data));
          } else {
            $.get("/static/wiki/plugins/inputs/getAllTmpl.html", function(tmpl) {
              e.html($.templates('getAllTmpl', tmpl).render(data));
            });
          }
        } else {
          e.text("");
        }
      },
      error: function() { e.text("!!!"); }
    })
  })

  $('span[data-url][data-variant!=all].dw-input').each(function() {
    var e = $(this);

    $.ajax({
      url: e.attr('data-url'),
      type: 'GET',
      contentType: "application/json",
      success: function(data, st, xhr) {
        if (xhr.status == 200) {
          e.text(data);
        } else {
          e.text("");
        }
      },
      error: function() { e.text("!!!"); }
    })
  })

  $('input[type=file][data-url].dw-input').change(function() {
    var n = $(this).files.length;
    var data = [];

    for (var i = 0; i < n; i++) {
      var file = this.files[i];
      var reader = new FileReader();

      reader.onload = function(ev) {
        data.push({
          name:file.name,
          size:file.size,
          type:file.type,
          content:ev.target.result
        });

        if (data.length == n) {
          wiki_input_post_data($(this).attr('data-url'), data);
        }
      }
      reader.readAsBinaryString(file);
    }
  })

  $('input[type=file][data-url].dw-input').each(function() {
    $(this).prop('disabled', false);
  })

  $('input[type!=file][data-url].dw-input').change(function() {
    wiki_input_post_data($(this).attr('data-url'), $(this).val());
  })

  $('input[type!=file][data-url].dw-input').each(function() {
    var field = $(this);
    wiki_input_get_data(field, function(data){
      field.val(data);
      field.prop('disabled', false);
    })
  })

  $('textarea[data-url].dw-input').change(function() {
    wiki_input_post_data($(this).attr('data-url'), $(this).val());
  })

  $('textarea[data-url].dw-input').each(function() {
    var field = $(this);
    wiki_input_get_data(field, function(data){
      field.val(data);
      field.prop('disabled', false);
    })
    wiki_input_get_data($(this));
  })

})
