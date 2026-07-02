import sys
import traceback
import re
def has_func(name):
    # 1. 处理 模块.函数 格式（math.sqrt）
    if "." in name:
        parts = name.split(".")
        obj = globals().get(parts[0])
        for p in parts[1:]:
            if not obj:
                break
            obj = getattr(obj, p, None)
    
    # 2. 处理普通名字（print / 自己定义的函数）
    else:
        obj = locals().get(name) or globals().get(name)
        if not obj:
            # 兼容内置（print / len）
            obj = __builtins__.get(name) if isinstance(__builtins__, dict) else getattr(__builtins__, name, None)

    # 重点：这里强制返回 True 或 False，永远不会返回 None！
    return callable(obj)
              

def Charlotte(*a,openname=False,opendef=False,opendeferr=True,opencode=False,defright=False):
    if not a:
        a = 'Charlotte'
    else:
        a = ''.join(str(x) for x in a)
        
    print('\n'+'==='*3+a+'==='*3)
    frame = sys._getframe(1)
    filename = frame.f_code.co_filename
    
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    lined = []
    lichar = []

    goodname={}  
    badname=[]
    
    defname=[]
    for i in lines:
        if ('Charlotte(' in i[0 : len('Charlotte(')] and ')' in i) or 'Charlotte import' in i:
            lichar.append(i)

        else:
            s = i.find('=')
            sl=i[0 : s]
            ls=i[s+1 : ]
            if (s != -1) and (i[s+1] != '=') and ('"' not in sl) and ("'" not in sl) and ('#' not in sl):
                
                name = i.split('=')[0].strip()

                name = name.replace(' ', '')  # 去除空格
                ls = ls.replace(' ', '')  # 去除空格

                goodname[name]=ls
                if openname:
                    print('\n')
                    print('---'*12)
                    print(f'原文件变量名: {sl}, 赋值: {ls}')                            
                    print(f"插值变量名: {name} 已被记录,值{goodname[name]}")
                    print('---'*12)

            else:
                badname.append(i)
  
            j = i.find('(')
            jl=i[0 : j]
            

            if (j != -1) and ('"' not in jl) and ("'" not in jl) and ('#' not in jl):
               jl = jl.replace(' ', '')
               if 'def' in jl:
                   jl = jl.replace('def', '').strip()
                   defname.append(jl)
                   lined.append(i)
                   continue

               elif jl in defname:
                    lastname = True                      
               else:
                    lastname = has_func(jl)
               if defright:
                 print(f'查找函数{jl}，结果: {lastname}')

               if not lastname:
                  lj= i[j+1 : -2]

                  

                  if i[-2] == ')':
                      txt = lj.split(',')
                      text=''
                      textnum=0
                      for t in txt:
                        t = t.replace(' ', '')
                        t = t.replace('"', '')
                        t = t.replace("'", '')
                        
                        vue = has_func(str(t))
                        if not vue and t in defname:
                            vue = True
 
                        if vue:
                          text+= t+'('
                          textnum+=1
                          if opendef:
                            print(f'{t}函数正确')
                        else:
                          if opendeferr:
                            print(f'{t}函数调用错误，跳过执行,函数表{lj}') 
                      if jl in goodname:
                          jl=goodname[jl]
                      else:
                          jl="'" + str(jl) + "'"
                      text +=jl[0 :  ] + ')' * textnum
                      if opendef:
                        print(f"转义后逻辑{text}")
                        
                      i=text+'\n'    
        lined.append(i)    

                      
                      
    for i in lichar:
        if i in lined:
            lined.remove(i)
        
            
    code = ''.join(lined)
    if opencode:
        print("=== 完整源码 ===")
        print(code,'\n')

    exec(code)
   
    sys.exit()



   



