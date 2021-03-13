$("[data-toggle=popover]").popover();

$(document).on('click', '.pdfDropdown', function (e) {
  e.stopPropagation();
});


$(".taskUpdate").click(function () {
    var ids = $(this).attr('data-id');
    var res = $(this).attr('data-result');
    var task = $(this).attr('data-title');
    $("#title").val( task );
    $("#detail").val( res );
    $("#ids").val( ids );
    $("#typeToUpdate").val( "Task" );
    $("#myModalLabel").html( "Edit Task" );
    $('#editModal').modal('show');
});

$(".sessionUpdate").click(function () {
    var ids = $(this).attr('data-id');
    var res = $(this).attr('data-result');
    var task = $(this).attr('data-title');
    $("#title").val( task );
    $("#detail").val( res );
    $("#ids").val( ids );
    $("#typeToUpdate").val( "Session" );
    $("#myModalLabel").html( "Edit Session" );
    $('#editModal').modal('show');
});

$(".setUpdate").click(function () {
    var ids = $(this).attr('data-id');
    var not = $(this).attr('data-note');
    var tit = $(this).attr('data-title');
    $("#title").val( tit );
    $("#detail").val( not );
    $("#ids").val( ids );
    $("#typeToUpdate").val( "Set" );
    $("#myModalLabel").html( "Edit Set" );
    $('#editModal').modal('show');
});

$(".projectUpdate").click(function () {
    var ids = $(this).attr('data-id');
    var not = $(this).attr('data-description');
    var tit = $(this).attr('data-title');
    var com = $(this).attr('data-company');
    var eng = $(this).attr('data-engineer');
    $("#projTitle").val( tit );
    $("#projDetail").val( not );
    $("#company").val( com );
    $("#engineer").val( eng );
    $("#projIds").val( ids );
    $("#projTypeToUpdate").val( "Project" );
    $("#myModalLabel").html( "Edit Project" );
    $('#editProjectModal').modal('show');
});


$(".passingIDforDelete").click(function () {
    var ids = $(this).attr('data-id');
    var task = $(this).attr('data-title');
    $("#deleteLabel").html( task );
    $("#idd").val( ids );
    $('#deleteModal').modal('show');
});

$(".delete").click(function () {
    var type = $(this).attr('data-type');
    var ids = $(this).attr('data-id');
    var title = $(this).attr('data-title');
    $("#deleteLabel").html( title );
    $("#idd").val( ids );
    $("#typeToDelete").val( type );
    $("#modalDeleteLabel").html( 'Are you sure you want to permanently remove this ' + type + '?')
    $('#deleteModal').modal('show');
});

$(".projDelete").click(function () {
    var type = $(this).attr('data-type');
    var ids = $(this).attr('data-id');
    var title = $(this).attr('data-title');
    $("#deleteLabel").html( title );
    $("#projIdd").val( ids );
    $("#projTypeToDelete").val( type );
    $("#modalDeleteLabel").html( 'Are you sure you want to permanently remove this ' + type + '?')
    $('#deleteModal').modal('show');
});


$(".refresh").click(function() {
  var type = $(this).attr('data-type');
  var ids = $(this).attr('data-id');
  console.log(type)
  $('#refreshModal').modal('show');
  $.ajax({
  type: 'POST',
  contentType: 'application/json',
  data: JSON.stringify({"Type": type, "id":ids}),
  dataType: 'json',
  url: '/refresh',
  success: function (response) {
      console.log(response)
      window.location = response;
  }});
})

$('#exportPDF').click(function() {
  var noteCh = false
  var logCh = false
  var taskCh = false
  var ses_id = $('#notesCheckPDF').attr("data-ses_id")
  if ($('#notesCheckPDF').is(':checked')) {noteCh = true}
  if ($('#logsCheckPDF').is(':checked')) {logCh = true}
  if ($('#tasksCheckPDF').is(':checked')) {taskCh = true}
  $.ajax({
  type: 'POST',
  contentType: 'application/json',
  data: JSON.stringify({"notes": noteCh, "logs": logCh, "tasks": taskCh, "ses_id":ses_id}),
  dataType: 'json',
  url: '/savepdf',
  success: function (rdhex) {
      console.log("Saved!")
      window.location.href = '/static/export/' + rdhex + '.pdf';
  }});
})


$(".logUpdate").click(function () {
    var ids = $(this).attr('data-id');
    var not = $(this).attr('data-note');
    var tit = $(this).attr('data-title');
    $("#title").val( tit );
    $("#detail").val( not );
    $("#ids").val( ids );
    $("#typeToUpdate").val( "Log" );
    $("#myModalLabel").html( "Edit Log" );
    $('#editModal').modal('show');
});

$(".loading").click(function () {
    $('#loadingModal').modal('show');
});


$('#inputGroupFile01').change(function() {
  var selectedFiles = $('#inputGroupFile01').prop("files")
  var names = $.map(selectedFiles, function(val) { return val.name; });
  names = names.toString();
  $('#selectedFile').text(names)
})

$('#lightThemeCheck').change(function() {
  var light = "light"
  if($(this).is(":checked")) {
    light = "light"
  } else {
    light = "dark"
  }
  $.ajax({
  type: 'POST',
  contentType: 'application/json',
  data: JSON.stringify({"lightTheme":light}),
  dataType: 'json',
  url: '/settings',
  success: function () {
      console.log("Added")
  }});
})


$('#addDefTopic').click(function() {
  var topText = $('#defTopicInput').val();
  $('#defaultTopicsTable tbody').append("<tr><td>" + topText + "</td><td>" +
  "<button type='button' class='btn btn-sm float-right' style='border: 0px; color: white;' id='deleteDefTopic'><i class='fa fa-times'></i></button>" +
  "</td></tr>");
  $('#defTopicInput').val("")

  defTopicTable = [];
  $('#defaultTopicsTable tbody tr').each(function() {
    tr = [];
    $(this).children('td').each(function() {
      tr.push($(this).text());
    })
    defTopicTable.push(tr[0])
  })
  $.ajax({
  type: 'POST',
  contentType: 'application/json',
  data: JSON.stringify({"Topics":defTopicTable}),
  dataType: 'json',
  url: '/settings',
  success: function () {
      console.log("Added")
  }});

})

$("#defaultTopicsTable").on('click', '#deleteDefTopic', function () {
  $(this).closest("tr").remove();

  defTopicTable = [];
  $('#defaultTopicsTable tbody tr').each(function() {
    tr = [];
    $(this).children('td').each(function() {
      tr.push($(this).text());
    })
    defTopicTable.push(tr[0])
  })
  $.ajax({
  type: 'POST',
  contentType: 'application/json',
  data: JSON.stringify({"Topics":defTopicTable}),
  dataType: 'json',
  url: '/settings',
  success: function () {
      console.log("Added")
  }});

});


var topicLeft = "data";
var setLeft = "set";
$(".addLeftButton").click(function () {
    var text = $('#inputParameterSelectLeft option:selected').text();
    $('#tableLeft tbody').append("<tr><td style='display:none'>" + topicLeft + "</td><td>" + setLeft + "</td><td>" + text +
    "<button type='button' class='btn btn-sm float-right' id='deleteLeftRow' style='border: 0px; color: white;'><i class='fa fa-times'></i></button>" +
    "</td></tr>");
});

$("#tableLeft").on('click', '#deleteLeftRow', function () {
  $(this).closest("tr").remove();
});


$('#inputParameterSetLeft').change(function() {
  var set = $(this).val();
  console.log(set)
  var topics = $(this).attr('data-topics').replace(/'/g, '"');
  topics = JSON.parse(topics)[set];
  var keys = Object.keys(topics);

  $('#inputTopicLeft').empty();
  $("#inputParameterSelectLeft").empty();
  $.each(keys, function(index, value) {
    $('#inputTopicLeft').append($('<a type="button" class="dropdown-item topicSelectedLeft" data-name=' + value + ' data-set=' + set + '>' + value + '</a>'))
  })

})

$(document.body).on("click", ".topicSelectedLeft", function () {
    setLeft = $(this).attr('data-set');
    topicLeft = $(this).attr('data-name');
    var topics = $("#inputTopicLeft").attr('data-params').replace(/'/g, '"');
    params = JSON.parse(topics)[setLeft][topicLeft];

    var parArr = [];
    for (x of params) {
      parArr.push(x.split("__-__")[1])
    }

    $('#inputParameterSelectLeft').empty()

    $.each(parArr, function(index, value) {
      $('#inputParameterSelectLeft')
         .append($("<option />").val(index).text(value));
       });
});


var topicRight = "data";
var setRight = "set";
$(".addRightButton").click(function () {
    var text = $('#inputParameterSelectRight option:selected').text();
    $('#tableRight tbody').append("<tr><td style='display:none'>" + topicRight + "</td><td>" + setRight + "</td><td>" + text +
    "<button type='button' class='btn btn-sm float-right' id='deleteRightRow' style='border: 0px; color: white;'><i class='fa fa-times'></i></button>" +
    "</td></tr>");
});

$("#tableRight").on('click', '#deleteRightRow', function () {
  $(this).closest("tr").remove();
});


$('#inputParameterSetRight').change(function() {
  var set = $(this).val();
  var topics = $(this).attr('data-topics').replace(/'/g, '"');
  topics = JSON.parse(topics)[set];
  var keys = Object.keys(topics);

  $('#inputTopicRight').empty();
  $("#inputParameterSelectRight").empty();
  $.each(keys, function(index, value) {
    $('#inputTopicRight').append($('<a type="button" class="dropdown-item topicSelectedRight" data-name=' + value + ' data-set=' + set + '>' + value + '</a>'))
  })

})

$(document.body).on("click", ".topicSelectedRight", function () {
    setRight = $(this).attr('data-set');
    topicRight = $(this).attr('data-name');
    var topics = $("#inputTopicRight").attr('data-params').replace(/'/g, '"');
    params = JSON.parse(topics)[setRight][topicRight];

    var parArr = [];
    for (x of params) {
      parArr.push(x.split("__-__")[1])
    }

    $('#inputParameterSelectRight').empty()

    $.each(parArr, function(index, value) {
      $('#inputParameterSelectRight')
         .append($("<option />").val(index).text(value));
       });
});


var topicFilter1 = "data";
var setFilter1 = "set";
$(document.body).on("click", ".topicSelectedfil1", function () {
  setFilter1 = $(this).attr('data-set');
  topicFilter1 = $(this).attr('data-name');
  var topics = $("#inputTopicfil1").attr('data-params').replace(/'/g, '"');
  params = JSON.parse(topics)[setFilter1][topicFilter1];

  var parArr = [];
  for (x of params) {
    parArr.push(x.split("__-__")[1])
  }

    $('#inputParameterSelectfil1').empty()
    $.each(parArr, function(index, value) {
    $('#inputParameterSelectfil1')
         .append($("<option />").val(index).text(value));
       });
});

$('#inputParameterSetfil1').change(function() {
  var set = $(this).val();
  var topics = $(this).attr('data-topics').replace(/'/g, '"');
  topics = JSON.parse(topics)[set];
  var keys = Object.keys(topics);

  $('#inputTopicfil1').empty();
  $("#inputParameterSelectfil1").empty();
  $.each(keys, function(index, value) {
    $('#inputTopicfil1').append($('<a type="button" class="dropdown-item topicSelectedfil1" data-name=' + value + ' data-set=' + set + '>' + value + '</a>'))
  })
})

var topicFilter2 = "data";
var setFilter2 = "set";
$(document.body).on("click", ".topicSelectedfil2", function () {
  setFilter2 = $(this).attr('data-set');
  topicFilter2 = $(this).attr('data-name');
  var topics = $("#inputTopicfil2").attr('data-params').replace(/'/g, '"');
  params = JSON.parse(topics)[setFilter2][topicFilter2];

  var parArr = [];
  for (x of params) {
    parArr.push(x.split("__-__")[1])
  }

    $('#inputParameterSelectfil2').empty()
    $.each(parArr, function(index, value) {
    $('#inputParameterSelectfil2')
         .append($("<option />").val(index).text(value));
       });
});

$('#inputParameterSetfil2').change(function() {
  var set = $(this).val();
  var topics = $(this).attr('data-topics').replace(/'/g, '"');
  topics = JSON.parse(topics)[set];
  var keys = Object.keys(topics);

  $('#inputTopicfil2').empty();
  $("#inputParameterSelectfil2").empty();
  $.each(keys, function(index, value) {
    $('#inputTopicfil2').append($('<a type="button" class="dropdown-item topicSelectedfil2" data-name=' + value + ' data-set=' + set + '>' + value + '</a>'))
  })
})

var topicFilter3 = "data";
var setFilter3 = "set";
$(document.body).on("click", ".topicSelectedfil3", function () {
  setFilter3 = $(this).attr('data-set');
  topicFilter3 = $(this).attr('data-name');
  var topics = $("#inputTopicfil3").attr('data-params').replace(/'/g, '"');
  params = JSON.parse(topics)[setFilter3][topicFilter3];

  var parArr = [];
  for (x of params) {
    parArr.push(x.split("__-__")[1])
  }

    $('#inputParameterSelectfil3').empty()
    $.each(parArr, function(index, value) {
    $('#inputParameterSelectfil3')
         .append($("<option />").val(index).text(value));
       });
});

$('#inputParameterSetfil3').change(function() {
  var set = $(this).val();
  var topics = $(this).attr('data-topics').replace(/'/g, '"');
  topics = JSON.parse(topics)[set];
  var keys = Object.keys(topics);

  $('#inputTopicfil3').empty();
  $("#inputParameterSelectfil3").empty();
  $.each(keys, function(index, value) {
    $('#inputTopicfil3').append($('<a type="button" class="dropdown-item topicSelectedfil3" data-name=' + value + ' data-set=' + set + '>' + value + '</a>'))
  })
})

var topicFilter4 = "data";
var setFilter4 = "set";
$(document.body).on("click", ".topicSelectedfil4", function () {
  setFilter4 = $(this).attr('data-set');
  topicFilter4 = $(this).attr('data-name');
  var topics = $("#inputTopicfil4").attr('data-params').replace(/'/g, '"');
  params = JSON.parse(topics)[setFilter4][topicFilter4];

  var parArr = [];
  for (x of params) {
    parArr.push(x.split("__-__")[1])
  }

    $('#inputParameterSelectfil4').empty()
    $.each(parArr, function(index, value) {
    $('#inputParameterSelectfil4')
         .append($("<option />").val(index).text(value));
       });
});

$('#inputParameterSetfil4').change(function() {
  var set = $(this).val();
  var topics = $(this).attr('data-topics').replace(/'/g, '"');
  topics = JSON.parse(topics)[set];
  var keys = Object.keys(topics);

  $('#inputTopicfil4').empty();
  $("#inputParameterSelectfil4").empty();
  $.each(keys, function(index, value) {
    $('#inputTopicfil4').append($('<a type="button" class="dropdown-item topicSelectedfil4" data-name=' + value + ' data-set=' + set + '>' + value + '</a>'))
  })
})

var topicFilter5 = "data";
var setFilter5 = "set";
$(document.body).on("click", ".topicSelectedfil5", function () {
  setFilter5 = $(this).attr('data-set');
  topicFilter5 = $(this).attr('data-name');
  var topics = $("#inputTopicfil5").attr('data-params').replace(/'/g, '"');
  params = JSON.parse(topics)[setFilter5][topicFilter5];

  var parArr = [];
  for (x of params) {
    parArr.push(x.split("__-__")[1])
  }

    $('#inputParameterSelectfil5').empty()
    $.each(parArr, function(index, value) {
    $('#inputParameterSelectfil5')
         .append($("<option />").val(index).text(value));
       });
});

$('#inputParameterSetfil5').change(function() {
  var set = $(this).val();
  var topics = $(this).attr('data-topics').replace(/'/g, '"');
  topics = JSON.parse(topics)[set];
  var keys = Object.keys(topics);

  $('#inputTopicfil5').empty();
  $("#inputParameterSelectfil5").empty();
  $.each(keys, function(index, value) {
    $('#inputTopicfil5').append($('<a type="button" class="dropdown-item topicSelectedfil5" data-name=' + value + ' data-set=' + set + '>' + value + '</a>'))
  })
})

var topicFilter6 = "data";
var setFilter6 = "set";
$(document.body).on("click", ".topicSelectedfil6", function () {
  setFilter6 = $(this).attr('data-set');
  topicFilter6 = $(this).attr('data-name');
  var topics = $("#inputTopicfil6").attr('data-params').replace(/'/g, '"');
  params = JSON.parse(topics)[setFilter6][topicFilter6];

  var parArr = [];
  for (x of params) {
    parArr.push(x.split("__-__")[1])
  }

    $('#inputParameterSelectfil6').empty()
    $.each(parArr, function(index, value) {
    $('#inputParameterSelectfil6')
         .append($("<option />").val(index).text(value));
       });
});

$('#inputParameterSetfil6').change(function() {
  var set = $(this).val();
  var topics = $(this).attr('data-topics').replace(/'/g, '"');
  topics = JSON.parse(topics)[set];
  var keys = Object.keys(topics);

  $('#inputTopicfil6').empty();
  $("#inputParameterSelectfil6").empty();
  $.each(keys, function(index, value) {
    $('#inputTopicfil6').append($('<a type="button" class="dropdown-item topicSelectedfil6" data-name=' + value + ' data-set=' + set + '>' + value + '</a>'))
  })
})

$("#sendData").click(function() {
  $('#loadingChartModal').modal('show');

  var set_id = {"type":$("#navBarLogNr").attr("data-type"), "id":$("#navBarLogNr").attr("data-id")};
  console.log(set_id)
  tableRight = [];
  $('#tableRight tbody tr').each(function() {
    tr = [];
    $(this).children('td').each(function() {
      tr.push($(this).text());
    })
    console.log(tr);
    name = setRight + "__-__" + tr[2] + "__-__" + tr[0];
    console.log(name)
    tableRight.push(name)
  })

  tableLeft = [];
  $('#tableLeft tbody tr').each(function() {
    tr = [];
    $(this).children('td').each(function() {
      tr.push($(this).text());
    })
    console.log(tr);
    name = setLeft + "__-__" + tr[2] + "__-__" + tr[0];
    console.log(name)
    tableLeft.push(name)
  })

  var filters = {"filters": ["fil1","fil2","fil3","fil4"], "options":["1","0","-1","off"], "topics": {"fil1": [topicFilter1, setFilter1], "fil2": [topicFilter2, setFilter2], "fil3": [topicFilter3, setFilter3], "fil4": [topicFilter4,setFilter4]}}
  var filterDict = {}
  for (fil of filters["filters"]) {
    var parName = '#inputParameterSelect' + fil + ' option:selected'
    var par = $(parName).text();
    var top = filters["topics"][fil]
    for (opt of filters["options"]) {
      id = "#" + fil + "_" + opt
      if ( $(id).is(":checked") ) {
        filterDict[fil] = {"Topic":top,"Parameter":par,"Value":opt}
      }
    }
  }
  filterDict["fil5"] = {"Topic":[topicFilter5,setFilter5],"Parameter":$('#inputParameterSelectfil5 option:selected').text(),"Value": [$("#min5").val(),$("#max5").val()]}
  filterDict["fil6"] = {"Topic":[topicFilter6,setFilter6],"Parameter":$('#inputParameterSelectfil6 option:selected').text(),"Value": [$("#min6").val(),$("#max6").val()]}

  rgLeft = [$("#rangeFromLeft").val(),$('#rangeToLeft').val()]
  rgRight = [$("#rangeFromRight").val(),$('#rangeToRight').val()]

  var selectedData = {"left": tableLeft, "right": tableRight, "set_id":set_id, "filters": filterDict, "axisRange": {"left":rgLeft,"right":rgRight}}
  console.log("Send!")

  //$.post( "/postmethod", {
  //  javascript_data: JSON.stringify(selectedData)
  //});

  $.ajax({
  type: 'POST',
  contentType: 'application/json',
  data: JSON.stringify(selectedData),
  dataType: 'json',
  url: '/postmethod',
  success: function () {
      $('#loadingChartModal').modal('hide');
  }});

})


var arr;
$('#commitSetButton').click(function(){
    $('#loadingBasic').modal('show');
    arr = $('#LogsForSetTable').find('[type="checkbox"]:checked').map(function(){
          return $(this).closest('tr').find('th:nth-child(1)').text();
    }).get();

    setDict = {"logs": arr};
    $.ajax({
    type: 'POST',
    contentType: 'application/json',
    data: JSON.stringify(setDict),
    dataType: 'json',
    url: '/loadtopics',
    success: function (topics) {
      var topix = JSON.stringify(topics).replace(/'/g, '"');
      topix = JSON.parse(topix)
      $("#topicsOfSettTable tbody").empty();

      var keys = Object.keys(topix)
      console.log(keys)
      $.each(keys, function(index, value) {
        var ch = "";
        if (topix[value]) {
          ch = "checked"
        }
        $('#topicsOfSettTable tbody').append("<tr><td>" + value + "</td><td class='float-right'>" + "<input type='checkbox'" + ch + "></td></tr>");
      })
      $('#createSetButton').prop('disabled', false);
      $('#createSetButton').css({"border-color": "#5cb85c", "color": "white"});

      $('#loadingBasic').modal('hide');
    }});
});


var arr;
$('#createSetButton').click(function(){
    $('#loadingSetModal').modal('show');
    arr = $('#LogsForSetTable').find('[type="checkbox"]:checked').map(function(){
          return $(this).closest('tr').find('th:nth-child(1)').text();
    }).get();

    tops = $('#topicsOfSettTable').find('[type="checkbox"]:checked').map(function(){
          return $(this).closest('tr').find('td:nth-child(1)').text();
    }).get();

    setDict = {"logs": arr, "tops": tops, "title": $('#setTitle').val(), "notes": $('#setNotes').val()};
    session = $('#LogsForSetTable').attr('data-session_id');
    console.log(session)
    $.ajax({
    type: 'POST',
    contentType: 'application/json',
    data: JSON.stringify(setDict),
    dataType: 'json',
    url: '/new_set/' + session,
    success: function (response) {
        console.log(response)
        window.location = response;
    }});
});

$(document).ready(function(){
    $(".up,.down").click(function(){
        var row = $(this).parents("tr:first");
        if ($(this).is(".up")) {
            row.insertBefore(row.prev());
        } else {
            row.insertAfter(row.next());
        }
    });
});
