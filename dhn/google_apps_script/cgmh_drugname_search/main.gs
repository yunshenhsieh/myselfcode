function doGet() {
  return HtmlService.createHtmlOutputFromFile('index');
}

function searchSheet(drugCode){
  var url = '<google sheet URL>'
  var name = '<sheet page name>'
  var SpreadSheet = SpreadsheetApp.openByUrl(url);
  var SheetName = SpreadSheet.getSheetByName(name);
  var targeRow = SheetName.getRange("D:D").createTextFinder(drugCode).matchEntireCell(true).findAll().map((r) => r.getA1Notation());
  if (targeRow.length >= 1){
    targeRow = parseInt(targeRow[0].slice(1, targeRow[0].length), 10);
    targeRow = SheetName.getSheetValues(targeRow,1,targeRow,SheetName.getLastColumn());
    return targeRow[0];
  }else{
    return drugCode + " 查無資料";
  }
  
}

function searchProductCode(productCode){
  var url = '<google sheet URL>'
  var name = '<sheet page name>'
  var SpreadSheet = SpreadsheetApp.openByUrl(url);
  var SheetName = SpreadSheet.getSheetByName(name);
  var targeRow = SheetName.getRange("A:A").createTextFinder(productCode).matchEntireCell(true).findAll().map((r) => r.getA1Notation());
  if (targeRow.length >= 1){
    targeRow = parseInt(targeRow[0].slice(1, targeRow[0].length), 10);
    targeRow = SheetName.getSheetValues(targeRow,1,targeRow,SheetName.getLastColumn());
    return targeRow[0];
  }else{
    return productCode + " 查無資料";
  }
  
}

function searchUpdateTime(){
  var url = '<google sheet URL>'
  var name = '<sheet page name>'
  var SpreadSheet = SpreadsheetApp.openByUrl(url);
  var SheetName = SpreadSheet.getSheetByName(name);
  var targeRow = SheetName.getRange("A:A").createTextFinder("更新時間").matchEntireCell(true).findAll().map((r) => r.getA1Notation());
  if (targeRow.length >= 1){
    targeRow = parseInt(targeRow[0].slice(1, targeRow[0].length), 10);
    targeRow = SheetName.getSheetValues(targeRow,1,targeRow,SheetName.getLastColumn());
    return targeRow[0];
  }else{
    return 
  }
  
}
