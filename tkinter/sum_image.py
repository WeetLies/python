from tkinter import *
from tkinter import filedialog
import tkinter.ttk as ttk
import tkinter.messagebox as msg
from PIL import Image
import os

root = Tk()
root.title("WeetLies GUI") #제목표시줄 지정

#파일 프레임 생성
file_frame=Frame(root)
file_frame.pack(fill="x",padx=5,pady=10)

#파일추가 
def add_file():
    files = filedialog.askopenfilenames(title="Select Image File",filetypes=(('PNG파일',"*.PNG"),('JPG파일',"*.jpg"),('BMP파일',"*.bmp"),('모든 파일',"*.*")),initialdir="C:/")
    
    # 사용자가 선택한 파일목록 리스트박스에 넣기
    for file in files:
        lstfile.insert(END,file)

#파일제거
def del_file():
    for index in reversed(lstfile.curselection()):
        lstfile.delete(index)

#저장경로
def path_line():
    fld_sel = filedialog.askdirectory()
    if fld_sel == '': #fld_sel를 열렸을때 취소 또는 그냥 닫기 버튼을 눌렀을떄
        return
    else:
        txt_dest_path.delete(0,END)
        txt_dest_path.insert(0, fld_sel)

#작업시작
def cmd_start():
    if lstfile.size() == 0: #파일목록에 데이터가 하나도 없으면
        msg.showwarning("경고","이미지 파일을 추가하세요!")
        return
    
    if len(txt_dest_path.get()) == 0: #저장경로가 지정되지 않았을때
        msg.showwarning("경고","저장경로를 선택하세요!")
        return
    
    #이미지 통합작업
    margin_image()

def margin_image():
    # print("Width : ",cmbx_width.get())
    # print("Margin : ",cmbx_margin.get())
    # print("Format : ",cmbx_format.get())
    try:
        img_width = cmbx_width.get()
        if img_width == 'Original': #Width 값을 original로 설정했을때는 
            img_width = -1 # -1일떄는 원본 기준
        else:
            img_width = int(img_width)

        img_space = cmbx_margin.get()
        # ['None','Small','Middle','Large']
        if img_space == "Small":
            img_space = 30
        elif img_space == "Middle":
            img_space = 60
        elif img_space == "Large":
            img_space = 90
        else:
            img_space = 0
        # ['PNG','JPG','BMP']
        img_for = cmbx_format.get().lower() # 값을 받아와서 소문자로 변경


        imgs = [Image.open(x) for x in lstfile.get(0,END)]

        # 이미지사이즈 리스트를 넣어서 하나씩 처리
        img_sz = [] 
        if img_width < 0:
            img_sz = [(x.size[0],x.size[1]) for x in imgs] #원본사용
        else:
            img_sz = [(int(img_width),int(x.size[1]*img_width/x.size[0])) for x in imgs]
        #예제 : 100* 60 의 이미지를 width 값을 80 으로 바꾸면 height 값은?
        #(원본width):(원본height) = (변경width):(변경height)
        # 100:60 = 80:?
        # x:y=x':y'
        #xy' =x'y
        #100y'=60*80
        #y'=4800/100
        #y'=48
        # x.size[0]:x.size[1]=img_width:?
        # x.size[0]?=x.size[1]*img_width
        # ? = x.size[1]*img_width/x.size[0]


        widths, heights = zip(*img_sz)
        print(widths,heights)

        max_width, total_height = max(widths),sum(heights)
        print(max_width)
        print(total_height)

        #새로운 이미지 생성
        if img_space > 0:
            total_height += (img_space * (len(imgs)-1))
        result_img = Image.new("RGB",(max_width,total_height),(255,255,255))
        y_offset = 0 # y 위치 좌표

        for idx, img in enumerate(imgs):
            #width가 원본이 아니면 이미지 크기 조절
            if img_width > -1: #원본이 아니면
                img = img.resize(img_sz[idx])#이미지크기 조절
            
            result_img.paste(img,(0,y_offset))
            y_offset += img.size[1]+img_space
            progress = (idx+1)/len(imgs) * 100 # 실제 percent정보 계산
            p_var.set(progress)
            progressbar.update()

        #포멧 옵션 처리
        fname="WeetLies."+ img_for
        dest_path = os.path.join(txt_dest_path.get(),fname)
        result_img.save(dest_path)
        msg.showinfo("저장완료","작업이 완료되었습니다,")
    except Exception as err: #예외처리
        msg.showerror("에러",err)



#파일추가 버튼 추가
btn_add_file = Button(file_frame,text="Add Files..",padx=10,pady=5,command=add_file)
btn_add_file.pack(side="left")

#파일제거 버튼 추가
btn_remove_file = Button(file_frame,text="Remove Files..",padx=10,pady=5,command=del_file)
btn_remove_file.pack(side="right")

#파일목록 프레임 생성
list_frame=Frame(root)
list_frame.pack(fill="both",padx=5,pady=5)
#스크롤바 생성
scrollbar = Scrollbar(list_frame)
scrollbar.pack(side="right",fill="y")
#파일리스트 리스트박스 생성
lstfile = Listbox(list_frame,selectmode="extended",width=5,yscrollcommand=scrollbar.set)
lstfile.pack(side="left",fill="both",expand=True)

#스크롤바 연동
scrollbar.config(command=lstfile.yview)

#파일저장위치 프레임 생성
path_frame =LabelFrame(root,text="Save Path:")
path_frame.pack(fill="x",padx=5,pady=5)

#파일경로 엔트리 생성
txt_dest_path = Entry(path_frame)
txt_dest_path.pack(side="left",fill="x",expand=True,padx=5,pady=5,ipadx=40)

#파일경로 버튼 생성
btn_dest_path = Button(path_frame,text="....",width=10,command=path_line)
btn_dest_path.pack(side="right",padx=5,pady=5)

#옵션 프레임 생성
option_frame = LabelFrame(root,text="Options")
option_frame.pack(fill="x",padx=5,pady=5)

#가로길이조절 라벨/콤보박스 생성
lbl_width = Label(option_frame,text="Width : ", width=7)
lbl_width.pack(side='left',padx=5,pady=5)
val_width = ['Original','1024','800','640']
cmbx_width = ttk.Combobox(option_frame,state="readonly",values=val_width,width=6)
cmbx_width.set(val_width[0])
cmbx_width.pack(side='left',padx=5,pady=5)

#여백 조절 라벨/콤보박스 생성
lbl_margin = Label(option_frame,text="Margin : ",width=7)
lbl_margin.pack(side="left",padx=5,pady=5)
val_margin =['None','Small','Middle','Large']
cmbx_margin = ttk.Combobox(option_frame,state="readyonly",values=val_margin,width=6)
cmbx_margin.set(val_margin[0])
cmbx_margin.pack(side="left",padx=5,pady=5)

#확장자 설정 라벨/콤보박스 생성
lbl_format = Label(option_frame,text="Format : ",width=10)
lbl_format.pack(side="left",padx=5,pady=5)
val_format = ['PNG','JPG','BMP']
cmbx_format = ttk.Combobox(option_frame,state="readonly",values=val_format,width=4)
cmbx_format.set(val_format[0])
cmbx_format.pack(side="left",padx=5,pady=5)

#프로그레스바 프레임 생성
bar_frame = Frame(root)
bar_frame.pack(fill="x",padx=5,pady=5)

#프로그레스바 생성 및 설정
p_var=DoubleVar()
progressbar = ttk.Progressbar(bar_frame,maximum=100,variable=p_var)
progressbar.pack(fill="x",padx=5,pady=5)

#작업프레임 생성
work_frame = Frame(root)
work_frame.pack(fill="x",padx=5,pady=5)

# 종료버튼 생성
btn_exit = Button(work_frame,text="Exit",command=root.quit,width=10)
btn_exit.pack(side="right",padx=5,pady=5)

# 시작버튼 생성
btn_start = Button(work_frame,text="Start",width=10,command=cmd_start)
btn_start.pack(side="right",padx=5,pady=5)

root.resizable(False,False) # 가로 세로 크기 변경 불가 반대식(.resizable(True,True)또는 생략)
root.mainloop()
