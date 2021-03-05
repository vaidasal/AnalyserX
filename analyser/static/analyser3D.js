var topicX = "data";
var setX = "set";

$('#inputParameterSetX').change(function() {
  var set = $(this).val();
  console.log(set)
  var topics = $(this).attr('data-topics').replace(/'/g, '"');
  topics = JSON.parse(topics)[set];
  var keys = Object.keys(topics);

  $('#inputTopicX').empty();
  $("#inputParameterSelectX").empty();
  $.each(keys, function(index, value) {
    $('#inputTopicX').append($('<a type="button" class="dropdown-item topicSelectedX" data-name=' + value + ' data-set=' + set + '>' + value + '</a>'))
  })

})

$(document.body).on("click", ".topicSelectedX", function () {
    setX = $(this).attr('data-set');
    topicX = $(this).attr('data-name');
    var topics = $("#inputTopicX").attr('data-params').replace(/'/g, '"');
    params = JSON.parse(topics)[setX][topicX];

    var parArr = [];
    for (x of params) {
      parArr.push(x.split("__-__")[1])
    }

    $('#inputParameterSelectX').empty()

    $.each(parArr, function(index, value) {
      $('#inputParameterSelectX')
         .append($("<option />").val(index).text(value));
       });
});

var topicY = "data";
var setY = "set";


$('#inputParameterSetY').change(function() {
  var set = $(this).val();
  console.log(set)
  var topics = $(this).attr('data-topics').replace(/'/g, '"');
  topics = JSON.parse(topics)[set];
  var keys = Object.keys(topics);

  $('#inputTopicY').empty();
  $("#inputParameterSelectY").empty();
  $.each(keys, function(index, value) {
    $('#inputTopicY').append($('<a type="button" class="dropdown-item topicSelectedY" data-name=' + value + ' data-set=' + set + '>' + value + '</a>'))
  })

})

$(document.body).on("click", ".topicSelectedY", function () {
    setY = $(this).attr('data-set');
    topicY = $(this).attr('data-name');
    var topics = $("#inputTopicY").attr('data-params').replace(/'/g, '"');
    params = JSON.parse(topics)[setY][topicY];

    var parArr = [];
    for (x of params) {
      parArr.push(x.split("__-__")[1])
    }

    $('#inputParameterSelectY').empty()

    $.each(parArr, function(index, value) {
      $('#inputParameterSelectY')
         .append($("<option />").val(index).text(value));
       });
});


var topicZ = "data";
var setZ = "set";


$('#inputParameterSetZ').change(function() {
  var set = $(this).val();
  console.log(set)
  var topics = $(this).attr('data-topics').replace(/'/g, '"');
  topics = JSON.parse(topics)[set];
  var keys = Object.keys(topics);

  $('#inputTopicZ').empty();
  $("#inputParameterSelectZ").empty();
  $.each(keys, function(index, value) {
    $('#inputTopicZ').append($('<a type="button" class="dropdown-item topicSelectedZ" data-name=' + value + ' data-set=' + set + '>' + value + '</a>'))
  })

})

$(document.body).on("click", ".topicSelectedZ", function () {
    setZ = $(this).attr('data-set');
    topicZ = $(this).attr('data-name');
    var topics = $("#inputTopicZ").attr('data-params').replace(/'/g, '"');
    params = JSON.parse(topics)[setZ][topicZ];

    var parArr = [];
    for (x of params) {
      parArr.push(x.split("__-__")[1])
    }

    $('#inputParameterSelectZ').empty()

    $.each(parArr, function(index, value) {
      $('#inputParameterSelectZ')
         .append($("<option />").val(index).text(value));
       });
});


var topicColor = "data";
var setColor = "";

$('#inputParameterSetColor').change(function() {
  var set = $(this).val();
  console.log(set)
  var topics = $(this).attr('data-topics').replace(/'/g, '"');
  topics = JSON.parse(topics)[set];
  var keys = Object.keys(topics);

  $('#inputTopicColor').empty();
  $("#inputParameterSelectColor").empty();
  $.each(keys, function(index, value) {
    $('#inputTopicColor').append($('<a type="button" class="dropdown-item topicSelectedColor" data-name=' + value + ' data-set=' + set + '>' + value + '</a>'))
  })

})

$(document.body).on("click", ".topicSelectedColor", function () {
    setColor = $(this).attr('data-set');
    topicColor = $(this).attr('data-name');
    var topics = $("#inputTopicColor").attr('data-params').replace(/'/g, '"');
    params = JSON.parse(topics)[setColor][topicColor];

    var parArr = [];
    for (x of params) {
      parArr.push(x.split("__-__")[1])
    }

    $('#inputParameterSelectColor').empty()
    $('#inputParameterSelectColor').append($("<option />"))

    $.each(parArr, function(index, value) {
      $('#inputParameterSelectColor')
         .append($("<option />").val(index).text(value));
       });
});

$("#table3D").on('click', '#delete3DRow', function () {
  $(this).closest("tr").remove();
});

$(".add3DButton").click(function () {
    var textX = $('#inputParameterSelectX option:selected').text();
    var textY = $('#inputParameterSelectY option:selected').text();
    var textZ = $('#inputParameterSelectZ option:selected').text();
    var textColor = $('#inputParameterSelectColor option:selected').text();
    $('#table3D tbody').append("<tr><td style='display:none'>" + topicX + "</td><td>" + setX + "</td><td>" + textX +
    "</td><td style='display:none'>" + topicY + "</td><td>" + setY + "</td><td>" + textY +
    "</td><td style='display:none'>" + topicZ + "</td><td>" + setZ + "</td><td>" + textZ +
    "</td><td style='display:none'>" + topicColor + "</td><td>" + setColor + "</td><td>" + textColor + "</td><td>" +
    "<button type='button' class='btn btn-sm btn-outline-secondary float-right' id='delete3DRow' style='border: 0px; color: white;'><i class='fa fa-times'></i></button>" +
    "</td></tr>");
});


$("#simulate3DData").click(function() {
  $('#loadingChartModal').modal('show');

  var set_id = {"type":$("#navBarLogNr").attr("data-type"), "id":$("#navBarLogNr").attr("data-id")};
  console.log(set_id)
  tableX = [];
  tableY = [];
  tableZ = [];
  tableC = [];
  $('#table3D tbody tr').each(function() {
    tr = [];
    $(this).children('td').each(function() {
      tr.push($(this).text());
    })
    console.log(tr);
    namex = tr[1] + "__-__" + tr[2] + "__-__" + tr[0];
    namey = tr[4] + "__-__" + tr[5] + "__-__" + tr[3];
    namez = tr[7] + "__-__" + tr[8] + "__-__" + tr[6];
    if (tr[11] == "") {
      namec = "";
    } else {
      namec = tr[10] + "__-__" + tr[11] + "__-__" + tr[9];
    }
    tableX.push(namex)
    tableY.push(namey)
    tableZ.push(namez)
    tableC.push(namec)
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

  startT = $("#startTime").val()
  if (startT == "") {
    startT = $("#startTime").attr("data-start")
  }

  endT = $("#endTime").val()
  if (endT == "") {
    endT = $("#endTime").attr("data-end")
  }
  timeSE = [startT,endT]
  tail = $('#tail3D').val()

  rgLeft = [$("#rangeFromLeft").val(),$('#rangeToLeft').val()]
  rgRight = [$("#rangeFromRight").val(),$('#rangeToRight').val()]

  var selectedData = {"X": tableX, "Y": tableY, "Z": tableZ, "Color": tableC, "timeSEList": timeSE, "action": "Sim", "tail": tail, "set_id":set_id, "filters": filterDict, "axisRange": {"left":rgLeft,"right":rgRight}}
  console.log(selectedData)

  $.ajax({
  type: 'POST',
  contentType: 'application/json',
  data: JSON.stringify(selectedData),
  dataType: 'json',
  url: '/chart3D',
  success: function () {
      $('#loadingChartModal').modal('hide');
  }});

})


$("#send3DData").click(function() {
  $('#loadingChartModal').modal('show');

  var set_id = {"type":$("#navBarLogNr").attr("data-type"), "id":$("#navBarLogNr").attr("data-id")};
  console.log(set_id)
  tableX = [];
  tableY = [];
  tableZ = [];
  tableC = [];
  $('#table3D tbody tr').each(function() {
    tr = [];
    $(this).children('td').each(function() {
      tr.push($(this).text());
    })
    console.log(tr);
    namex = tr[1] + "__-__" + tr[2] + "__-__" + tr[0];
    namey = tr[4] + "__-__" + tr[5] + "__-__" + tr[3];
    namez = tr[7] + "__-__" + tr[8] + "__-__" + tr[6];
    if (tr[11] == "") {
      namec = "";
    } else {
      namec = tr[10] + "__-__" + tr[11] + "__-__" + tr[9];
    }
    tableX.push(namex)
    tableY.push(namey)
    tableZ.push(namez)
    tableC.push(namec)
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

  startT = $("#startTime").val()
  if (startT == "") {
    startT = $("#startTime").attr("data-start")
  }

  endT = $("#endTime").val()
  if (endT == "") {
    endT = $("#endTime").attr("data-end")
  }
  timeSE = [startT,endT]
  tail = $('#tail3D').val()

  rgLeft = [$("#rangeFromLeft").val(),$('#rangeToLeft').val()]
  rgRight = [$("#rangeFromRight").val(),$('#rangeToRight').val()]

  var selectedData = {"X": tableX, "Y": tableY, "Z": tableZ, "Color": tableC, "timeSEList": timeSE, "action": "Chart", "tail": tail, "set_id":set_id, "filters": filterDict, "axisRange": {"left":rgLeft,"right":rgRight}}
  console.log(selectedData)

  $.ajax({
  type: 'POST',
  contentType: 'application/json',
  data: JSON.stringify(selectedData),
  dataType: 'json',
  url: '/chart3D',
  success: function () {
      $('#loadingChartModal').modal('hide');
  }});

})

$('#analyserSettings').click(function() {
  $('#loadingBasic').modal('show');
  $('.analyser2D').hide();
  $('.analyser3D').hide();

  var id = $('#navBarLogNr').attr('data-id')
  var type = $('#navBarLogNr').attr('data-type')

  if (type == "log") {
    $.ajax({
    type: 'POST',
    contentType: 'application/json',
    data: JSON.stringify({"type": type, "id": id}),
    dataType: 'json',
    url: '/datasettings',
    success: function (topics) {
      var topix = JSON.stringify(topics).replace(/'/g, '"');
      topix = JSON.parse(topix)
      $("#topicsSettTable tbody").empty();

      var keys = Object.keys(topix)
      console.log(keys)
      $.each(keys, function(index, value) {
        var ch = "";
        if (topix[value]) {
          ch = "checked"
        }
        $('#topicsSettTable tbody').append("<tr><td>" + value + "</td><td class='float-right'>" + "<input type='checkbox'" + ch + "></td></tr>");
      })

      $('.analyserSettings').show();
      $('#analyser2DButton').css({"background-color": "transparent", "border-color": "transparent"});
      $('#analyser3DButton').css({"background-color": "transparent", "border-color": "transparent"});
      $('#analyserSettings').css({"background-color": "#363636", "border-color": "#363636"});
      $('#loadingBasic').modal('hide');
    }});
  } else {
    $("#topicsSettTable tbody").empty();
    var logIds = JSON.parse($('#topicsSettTable').attr("data-logIds"));
    var setId = $('#topicsSettTable').attr("data-id");

    $.ajax({
    type: 'POST',
    contentType: 'application/json',
    data: JSON.stringify({"logs": logIds, "setId": setId}),
    dataType: 'json',
    url: '/loadtopics',
    success: function (topics) {
      var topix = JSON.stringify(topics).replace(/'/g, '"');
      topix = JSON.parse(topix)
      $("#topicsSettTable tbody").empty();

      var keys = Object.keys(topix)
      console.log(keys)
      $.each(keys, function(index, value) {
        var ch = "";
        if (topix[value]) {
          ch = "checked"
        }
        $('#topicsSettTable tbody').append("<tr><td>" + value + "</td><td class='float-right'>" + "<input type='checkbox'" + ch + "></td></tr>");
      })

      $('.analyserSettings').show();
      $('#analyser2DButton').css({"background-color": "transparent", "border-color": "transparent"});
      $('#analyser3DButton').css({"background-color": "transparent", "border-color": "transparent"});
      $('#analyserSettings').css({"background-color": "#363636", "border-color": "#363636"});
      $('#loadingBasic').modal('hide');
    }});
  }
})

$('#saveSettTopics').click(function() {
  var type = $('#topicsSettTable').attr("data-type")
  if (type == "set") {
    $('#loadingSetModal').modal('show');
  } else {
    $('#loadingBasic').modal('show');
  }
  var id = $('#topicsSettTable').attr("data-id")

  arr = $('#topicsSettTable').find('[type="checkbox"]:checked').map(function(){
        return $(this).closest('tr').find('td:nth-child(1)').text();
  }).get();

  $.ajax({
  type: 'POST',
  contentType: 'application/json',
  data: JSON.stringify({"type": type,"id":id, "checkTopics": arr}),
  dataType: 'json',
  url: '/saveTopics',
  success: function (response) {
      console.log(response)
      window.location = response;
  }});
})

$('#analyser2DButton').click(function() {
  $('.analyser2D').show();
  $('.analyser3D').hide();
  $('.analyserSettings').hide();
  $('#analyserSettings').css({"background-color": "transparent", "border-color": "transparent"});
  $('#analyser3DButton').css({"background-color": "transparent", "border-color": "transparent"});
  $('#analyser2DButton').css({"background-color": "#363636", "border-color": "#363636"});
})

$('#analyser3DButton').click(function() {
  $('.analyser2D').hide();
  $('.analyserSettings').hide();
  $('.analyser3D').show();
  $('#analyserSettings').css({"background-color": "transparent", "border-color": "transparent"});
  $('#analyser2DButton').css({"background-color": "transparent", "border-color": "transparent"});
  $('#analyser3DButton').css({"background-color": "#363636", "border-color": "#363636"});
})
