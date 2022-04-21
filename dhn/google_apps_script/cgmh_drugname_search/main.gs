function doGet() {
  return HtmlService.createHtmlOutputFromFile('index');
}

function searchSheet(drugCode){
  var url = 'https://docs.google.com/spreadsheets/d/1eFLyfaSQC8YXJ1mECZHhO2B2rVHpxfRUuiC5BROtnAQ/edit#gid=225650400'
  var name = 'drugfile'
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
  var url = 'https://docs.google.com/spreadsheets/d/1eFLyfaSQC8YXJ1mECZHhO2B2rVHpxfRUuiC5BROtnAQ/edit#gid=225650400'
  var name = 'drugfile'
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
