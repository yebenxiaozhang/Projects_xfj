imgs = 6
a = 1
all_imgs = {}
imgs1 = imgs + int(1)
print(imgs1)
print(all_imgs)
while a != imgs1:
    b = 'f' + str(a)
    print(b)
    files = 'file' + str(a)
    print(files)
    all_imgs[files] = ('购房版APP-750x1334-0.png', b, 'image/jpeg')
    b = open('D:\\PycharmProjects\\XFJ\\Agent_Api\\imgs\\购房版APP-750x1334-0.png', 'rb')
    a = a + 1
    print(all_imgs)
    print(b)

result = {'user':'sily','age':'18'}
#执行以下代码
result['day'] = '2019-06-20'
print(result)