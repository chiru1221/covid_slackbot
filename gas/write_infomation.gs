var debug = true
var skip_row = 2
var start_date = new Date(2021, 4-1, 1)
// sheet columns to numbers
var com_to_low = {"検温":3, "倦怠感の有無":4, "登校時間":5, "帰宅時間":6, "手洗いの有無":7}
var USER = {
    'Username': 'sheetname',
  }
// slack commands to sheet columns
var cm_to_col = {
    '/attend': '検温',
    '/arrive': '登校時間',
    '/homing': '帰宅時間',
    '/ventilate': '換気',
}

function doGet(e){
  var params = e.parameter
  print_log(params)
  html = ''
  if (params.name){
    html += JSON.stringify(params)
  }
  else{
    html += 'attributes are incorrect'
  }
  
  return HtmlService.createHtmlOutput(html)
}

function print_log(info) {
  // Logger.log(info)
  var name = USER[info.name]
  // if (info.command == '/ventilate'){

  // }
  // if (name == "研究室全体"){return -1}
  // var command = "登校時間"
  var command = cm_to_col[info.command]
  var date = new Date()
  var row = parseInt((date.getTime() - start_date.getTime())/(24*3600*1000)) + skip_row + 1
  if (debug){
    Logger.log(start_date)
    Logger.log(date)
    Logger.log(col)
  }

  if (command == '換気'){
    row = row - 1
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('研究室全体')
    if (debug){
      Logger.log(date.getHours().toString() + ":" + date.getMinutes().toString())
      Logger.log("row " + row)
      Logger.log("col " + col)
    }
    // 5: ドアの解放 6: 窓の解放, 7: 窓の解放時間
    is_ok = sheet.getRange(row, 5).getValue()
    if (is_ok == 'OK'){
      // From the second time onwards
      value = date.toTimeString().slice(0, 5)
      pre_value = sheet.getRange(row, 7).getValue().toString()
      if (pre_value != ''){
        if (!pre_value.includes(',')){
          pre_value = pre_value.slice(16, 21)
        }
        // pre_value = pre_value.split(', ')[0]
        value = pre_value + ', ' + value
      }
      sheet.getRange(row, 7).setValue(value)
    }
    else{
      // First time
      sheet.getRange(row, 5, 1, 2).setValue('OK')
    }
  }
  else{
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(name)
    var col = com_to_low[command]
    
    if (debug){
      Logger.log(date.getHours().toString() + ":" + date.getMinutes().toString())
      Logger.log("row " + row)
      Logger.log("col " + col)
    }
    value = date.toTimeString().slice(0, 5)
    if (col == 3){
      value = info.value
      sheet.getRange(row, 4).setValue('無')
    }
    else if(col == 5){
      sheet.getRange(row, 7).setValue('有')
    }
    sheet.getRange(row, col).setValue(value)
  }
}

