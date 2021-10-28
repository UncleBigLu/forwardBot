from botoy import Action, Botoy, GroupMsg
from botoy import decorators as deco
import os
import re


bot = Botoy()
fromGroup = os.environ['fromGroup']
toGroup = os.environ['toGroup']

botQQ = os.environ['botQQ']
action = Action(botQQ)

pattern = r'^(?=.*全体成员)(?=.*大学习).*$'
myRe = re.compile(pattern)
# Message with @全体成员 would cause ctx.Content in the format of a dict.
# Add a regex to judge if it's a dict and extract message from this dict string.
dictPattern = r'^\{"Content":"(.*)","UserExt".*\}$'
dictRe = re.compile(dictPattern)

@bot.group_context_use
def _(ctx):
    # Block msg except from masterQQ
    if str(ctx.FromGroupId) != fromGroup:
        return
    return ctx

@bot.on_group_msg
@deco.ignore_botself
def get_msg(ctx):

    action = Action(ctx.CurrentQQ)
    
    content = ctx.Content
    if(myRe.match(content)):
        m = dictRe.match(content)
        if(m != None):
            action.sendGroupText(int(toGroup), m.group(1))
        else:
            action.sendGroupText(int(toGroup), content)


if __name__ == '__main__':
    bot.run()
