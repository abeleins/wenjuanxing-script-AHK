#IfWinActive ahk_exe msedge.exe

F8::

	Loop
{
    Sleep, 2000  ; 等待2000毫秒，也就是2秒
	if GetColor(1217,1156)=="0x0095FF" { ; 点击确定
	Click, 1217,1156
	}
	if GetColor(1306,1180)=="0x0095FF" {
	Click, 1306,1180
	}
	if GetColor(1009,1929)=="0xE8E8E8" or GetColor(972,1917)=="0x809DC7"{
        MouseMove, 960,1911
        Sleep, 100
        MouseClick, left, , , 1, 0, D  ; 鼠标左键按下，但不释放
        Sleep, 100
        MouseMove, 1412,1922
        Sleep, 100
        MouseClick, left, , , 1, 0, U  ; 释放鼠标左键
	}
    Click, 1152, 1922  ; 在指定的屏幕坐标处进行点击GetColor(1152,1922)=="0xFFFFFF"GetColor(1412,1922)=="0xFFFFFF"
}
return


F9::stop := !stop
GetColor(x,y)
	{
	PixelGetColor, color, x, y, RGB
	StringRight color,color,10 ;
	return color
	}
	
