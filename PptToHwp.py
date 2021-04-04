import win32com.client as win32 
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilenames
from tkinter.filedialog import askdirectory
import os

from PIL import Image

from comtypes.client import Constants, CreateObject
#!pip install comtypes

def save_pptx_as_png(png_foldername: str, pptx_filename: str, overwrite_folder: bool = False):
    if os.path.isdir(png_foldername) and not overwrite_folder:
        print(f"Folder {png_foldername} already exists. "
              f"Set overwrite_folder=True, if you want to overwrite folder content.")
        return

    powerpoint = CreateObject("Powerpoint.Application")
    pp_constants = Constants(powerpoint)

    pres = powerpoint.Presentations.Open(pptx_filename)
    pres.SaveAs(png_foldername, pp_constants.ppSaveAsPNG)
    pres.close()
    if powerpoint.Presentations.Count == 0:  # only close, when no other Presentations are open!
        powerpoint.quit()

def getfiles():
    # %% 이미지파일 선택
    root=Tk()
    filelist=askopenfilenames()
    root.destroy()
    return filelist

def getdirpath():
    root = Tk()
    # root.withdraw()
    dir_path = askdirectory(parent=root,initialdir="/",title='Please select a directory')
    root.destroy()
    print(dir_path)
    return(dir_path)



def PngToHwp(dirpath):
    hwp=win32.Dispatch("HWPFrame.HwpObject")
    hwp.XHwpWindows.Item(0).Visible=True
    hwp.RegisterModule("FilePathCheckDLL", "FilePathCheckerModule")  # 보안모듈 적용(파일 열고닫을 때 팝업이 안나타남)
    #양식 변경 
    hwp.HAction.GetDefault("PageSetup", hwp.HParameterSet.HSecDef.HSet)
    hwp.HParameterSet.HSecDef.PageDef.LeftMargin = hwp.MiliToHwpUnit(0)
    hwp.HParameterSet.HSecDef.PageDef.RightMargin = hwp.MiliToHwpUnit(0)
    hwp.HParameterSet.HSecDef.PageDef.TopMargin = hwp.MiliToHwpUnit(0)
    hwp.HParameterSet.HSecDef.PageDef.BottomMargin = hwp.MiliToHwpUnit(0)
    hwp.HParameterSet.HSecDef.PageDef.HeaderLen = hwp.MiliToHwpUnit(0.0)
    hwp.HParameterSet.HSecDef.PageDef.FooterLen = hwp.MiliToHwpUnit(0.0)
    hwp.HParameterSet.HSecDef.PageDef.GutterLen = hwp.MiliToHwpUnit(0.0)
    hwp.HParameterSet.HSecDef.HSet.SetItem("ApplyClass", 24)
    hwp.HParameterSet.HSecDef.HSet.SetItem("ApplyTo", 3)  # 문서 전체 변경
    hwp.HAction.Execute("PageSetup", hwp.HParameterSet.HSecDef.HSet)

    filelist=os.listdir(dirpath)
    

    for file in filelist:
        filepath=os.path.join(dirpath,file)
        if os.path.splitext(filepath)[1]=='.PNG':
            
            # image = Image.open(filepath)
            #resize_image = image.resize((810 ,1140))
            # image.thumbnail((810 ,1140), Image.ANTIALIAS)
            # image.save(filepath)
 
            hwp.InsertPicture(filepath,True,2)
           
            
        else :print(file+"이미지 파일이 아닙니다.")
            
            
    dd="dddd.hwp"
    hwp.SaveAs(os.path.join(dirpath,dd))
    hwp.Quit()



if __name__ == "__main__":
    # dir=getdirpath()
    # PngToHwp(dir)


    ff=os.getcwd()
    filelist=os.listdir(ff)
    print(filelist[2])
    gkq=os.path.join(ff,"경부선_부강추풍령_제2권_요약5 한동욱_0826_5p_DCD_리사이즈완료한 최종파일있습니다_승호.pptx")
    enl=os.path.join(ff,"dd")
    
    print(gkq)
    save_pptx_as_png(enl,gkq,True)