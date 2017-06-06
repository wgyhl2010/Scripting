编译脚本调用方式如下:
python compile.py param1 param2 parm3

参数含义:
param1,初始化文件的全路径名称,如/root/compile/config.cfg,其中包含jdkhome的路径设置,具体设置参考当前目录下的config.cfg文件
param2,java源码所在的根目录,如/root/src/,在源码中如果依赖了jar包,则必须将jar放在src的lib目录下,否则找不到依赖
param3,java输出文件的位置,如/root/output

注意:
1.在进行编译时,一定要设置config文件中的jdkhome;
2.所有参数的路径都是绝对路径,不要使用相对路径;
3.对于编译的源文件目录一定不能含有空格
4.需要在config文件中配置生成jar包的名称,如test.jar,详情参考当前目录下的config.cfg文件

所编译的工程目录结构:
|-----src
       |-----edu.njupt....
       |-----config.properties
|-----lib
|-----MANIFEST.MF
