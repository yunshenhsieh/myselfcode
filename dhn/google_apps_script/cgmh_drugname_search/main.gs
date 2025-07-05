function doGet() {
  return HtmlService.createHtmlOutputFromFile('index');
}

function getSheetData() {
  const url = '<google sheet URL>';
  const name = '<sheet page name>';
  const SpreadSheet = SpreadsheetApp.openByUrl(url);
  const SheetName = SpreadSheet.getSheetByName(name);
  const data = SheetName.getDataRange().getValues();
  Logger.log(data);
  return (data);
}

function searchUpdateTime(){
  var url = '<google sheet URL>';
  var name = '<sheet page name>';
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
