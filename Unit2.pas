unit Unit2;

interface

uses
  System.SysUtils, System.Types, System.UITypes, System.Classes, System.Variants,
  FMX.Types, FMX.Controls, FMX.Forms, FMX.Graphics, FMX.Dialogs,
  FMX.Controls.Presentation, FMX.StdCtrls, FireDAC.Stan.Intf,
  FireDAC.Stan.Option, FireDAC.Stan.Error, FireDAC.UI.Intf, FireDAC.Phys.Intf,
  FireDAC.Stan.Def, FireDAC.Stan.Pool, FireDAC.Stan.Async, FireDAC.Phys,
  FireDAC.Phys.MSAcc, FireDAC.Phys.MSAccDef, FireDAC.FMXUI.Wait,
  FireDAC.Stan.Param, FireDAC.DatS, FireDAC.DApt.Intf, FireDAC.DApt,
  FMX.Memo.Types, FMX.ScrollBox, FMX.Memo, Data.DB, FireDAC.Comp.DataSet,
  FireDAC.Comp.Client;

type
  TForm2 = class(TForm)
    cerrar: TButton;
    FDConnection1: TFDConnection;
    FDQuery1: TFDQuery;
    DataSource1: TDataSource;
    Memo1: TMemo;
    buttoncargar: TButton;
    procedure cerrarClick(Sender: TObject);
    procedure buttoncargarClick(Sender: TObject);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  Form2: TForm2;

implementation

{$R *.fmx}

procedure TForm2.buttoncargarClick(Sender: TObject);
var i : Integer;
begin
  FDQuery1.Close;
  FDQuery1.SQL.Clear;
  FDQuery1.SQL.Add('select from * DataCursos');
  FDQuery1.Open();
  for i := 1 to FDQuery1.RecordCount do
  begin
    memo1.Lines.Add(FDQuery1.Fields[0].AsString+'  '
    );
  end;

end;

procedure TForm2.cerrarClick(Sender: TObject);
begin
Close;
end;

end.
