unit Unit1;

interface

uses
  System.SysUtils, System.Types, System.UITypes, System.Classes, System.Variants,
  FMX.Types, FMX.Controls, FMX.Forms, FMX.Graphics, FMX.Dialogs,
  FMX.Controls.Presentation, FMX.StdCtrls, FMX.Edit;

type
  TForm1 = class(TForm)
    Panel1: TPanel;
    Titulo: TLabel;
    pideCodigoCurso: TLabel;
    GuardaCodigo: TEdit;
    pideNombreCurso: TLabel;
    Edit1: TEdit;
    pideHoras: TLabel;
    guardaHoras: TEdit;
    GuardarCurso: TButton;
    CambiarVenetana: TButton;
    procedure CambiarVenetanaClick(Sender: TObject);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  Form1: TForm1;

implementation

{$R *.fmx}

uses Unit2;

procedure TForm1.CambiarVenetanaClick(Sender: TObject);
begin
Form2.ShowModal();
end;

end.
