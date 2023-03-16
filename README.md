## 效果演示:
<img src="https://www.cdnjson.com/images/2023/03/16/tutieshi_640x360_41s.gif" alt="tutieshi_640x360_41s.gif" border="0" />  
  
[English Version](https://github.com/Yudaotor/Riot-Accounts-AutoChangePassword/blob/master/README.EN.md)|
[中文版本](https://github.com/Yudaotor/Riot-Accounts-AutoChangePassword/blob/master/README.md)
# 本程序用于拳头账号自动修改密码(!使用强烈建议挂上VPN,不然加载速度很慢容易导致程序失败!)  
使用过程中有遇到什么问题可以联系我  
telegram: https://t.me/Yudaotor  
discord: Khalil#7843  
可以给我点个小星星吗(*^_^*)⭐  
  
  
**下载方法**,请点击右方的release中下载最新版的exe文件使用.
## 使用须知:
0. [已验证邮箱账号配置教程](https://github.com/Yudaotor/Riot-Accounts-AutoChangePassword/wiki/%E5%A6%82%E4%BD%95%E4%B8%BA%E9%AA%8C%E8%AF%81%E8%BF%87%E9%82%AE%E7%AE%B1%E7%9A%84%E8%B4%A6%E5%8F%B7%E8%87%AA%E5%8A%A8%E4%BF%AE%E6%94%B9%E5%AF%86%E7%A0%81(How-to-change-password-automatically-for-accounts-with-verified-emails))
1. 本程序支持微软edge浏览器和chrome谷歌浏览器,所以需要下载好自己浏览器对应的webdriver这个东西.具体如何下载并配置,大家自行谷歌.(注意需要下载与自己浏览器匹配的版本)
2. 需要进行修改密码的账号信息需要存储在txt文件中,具体格式为:  
213451231----351252312  
a21341----3512s5312  
213s51231----35s125312  
213451sd31----351sd52312  
3. **使用前需要先配置好config.yaml文件**  
(需要注意!!!文件路径中要使用\\\而非\\)  
(配置路径时,账号信息文件后面记得加.txt,driver后面记得加.exe)  
(路径不要出现中文以及中文字符)  
(如果没有验证过邮箱的话就不用填写imap的配置信息)
例子:  
![image](https://user-images.githubusercontent.com/87225219/225528615-44b2a7bd-4b87-4a40-8e69-fb5222c3abdc.png)

5. 程序执行后账号密码修改成功与否可以在log文件夹中查看.
6. 有无验证过邮箱的账号都可以使用.有验证过的需要在配置文件中加入对应的邮箱IMAP信息
## 程序运行控制台显示截图:
![image](https://user-images.githubusercontent.com/87225219/225540315-faa5d20f-1fb5-45d2-915f-ba695ca8be2a.png)
