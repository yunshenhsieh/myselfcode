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
