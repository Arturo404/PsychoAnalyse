from PIL import Image
import matplotlib.pyplot as plt





def pixel_average(x,y,image_rgb):
    value = 0
    for i in range(0,25):
        for j in range(0,25):
            #print(image_rgb.getpixel((x+i, y+j)),x+i,y+j)
            value += image_rgb.getpixel((x-i, y+j))[0]
    return value

def best_answer(x,y,image_rgb,z):
    index = 0
    minim = pixel_average(x,y,image_rgb)
    #print(minim)
    for i in range(1,4):
        temp = pixel_average(x-int(i*(40+z)),y,image_rgb)
        #print(temp)
        if temp<minim:
            minim = temp
            index = i
    return str(index+1)

def all_answer_serie(x,y,image_rgb,z):
    lst = []
    for i in range(23):
        #print("question n:",i+1,int(x+i*0.37),int(y+i*40.21))
        lst.append(best_answer(int(x+i*0.37),int(y+i*40.21),image_rgb,z))
    return lst

def first_pixel(image_rgb):
    value = 0
    for i in range(2255,2070,-1):
        for j in range(200,350):
            if image_rgb.getpixel((i,j))[0] == 0:
                    #and image_rgb.getpixel((i-1,j+1))[0] == 0 and image_rgb.getpixel((i,j+1))[0] == 0 and image_rgb.getpixel((i+1,j+1))[0] == 0 and image_rgb.getpixel((i-1,j))[0] == 0 and image_rgb.getpixel((i,j))[0] == 0 and image_rgb.getpixel((i+1,j))[0] == 0 and image_rgb.getpixel((i-1,j-1))[0] == 0 and image_rgb.getpixel((i,j-1))[0] == 0 and image_rgb.getpixel((i+1,j-1))[0] == 0:
                return i,j
    return 0,0

def lst_answer_exam(image_rgb):
    lst = []
    a,b = first_pixel(image_rgb)
    a -= 445
    b += 79
    lst.append(all_answer_serie(a,b,image_rgb,0))
    lst.append(all_answer_serie(a-284, b+1, image_rgb,0))
    lst.append(all_answer_serie(a-564, b+2, image_rgb,0))
    lst.append(all_answer_serie(a-853, b+2, image_rgb,0))
    lst.append(all_answer_serie(a-1137, b+3, image_rgb,0))
    lst.append(all_answer_serie(a-561, b+1251, image_rgb,0))
    lst.append(all_answer_serie(a-850, b+1251, image_rgb,0))
    lst.append(all_answer_serie(a-1132, b+1251, image_rgb,0))
    return lst

def good_answer(lst_good,image_rgb,histo):
    lst = []
    #answer = lst_answer_exam(image_rgb)
    answer = image_rgb
    for i in range(len(lst_good)):
        temp, count = 0,0
        for j in range(len(lst_good[i])):
            if answer[i][j]!=lst_good[i][j] and lst_good[i][j]!=5:
                temp+=1
            else:
                histo[i][j]+=1
            count+=1
        #lst.append("Serie "+str(i+1)+": "+str(count-temp)+"/"+str(count))
        lst.append((count-temp,count))
    return lst

def final_grade(lst_grade,lst_id_serie, redac_grade):
    ## id serie : 1--> Francais, 2--> Math, 3-->Anglais

    verbal = [50,51,53,54,56,57,59,60,62,63,65,67,69,71,74,76,78,81,84,87,90,93,96,98,101,104,106,109,111,114,117,120,123,125,128,131,134,138,142,146,150]
    quantitatif = [50,52,55,58,60,63,66,69,71,73,76,79,81,83,86,89,91,93,96,99,101,103,106,109,111,113,116,119,121,123,126,129,131,133,136,138,140,142,144,147,150]
    anglais = [50,51,52,54,55,57,58,59,61,63,65,67,69,71,73,75,78,80,82,85,88,90,92,95,98,100,102,104,107,110,112,114,117,120,122,124,127,130,132,135,138,141,144,147,150]
    grade_ver,num_verb = 0,0
    for i in lst_id_serie[0]:
        grade_ver+=int(round((lst_grade[i-1][0]/lst_grade[i - 1][1])*20))
    grade_ver = (verbal[grade_ver]-50)*0.75+50+2*redac_grade+1

    grade_quan,num_quan = 0,0
    for i in lst_id_serie[1]:
        grade_quan+=int(round((lst_grade[i-1][0]/lst_grade[i - 1][1])*20))
    grade_quan = quantitatif[grade_quan]

    grade_angl, num_angl = 0, 0
    for i in lst_id_serie[2]:
        grade_angl += int(round((lst_grade[i - 1][0] / lst_grade[i - 1][1]) * 22))
    grade_angl = anglais[grade_angl]

    final_grade = int(round(200+600*(grade_ver*2+grade_quan*2+grade_angl-250)/500))
    return [grade_ver,grade_quan,grade_angl,final_grade]


def all_student(lst_answer,max_id,id_serie,lst_redac_grade,lst_all_grades):
    lst = []
    histo = [[0]*23,[0]*23,[0]*23,[0]*23,[0]*23,[0]*23,[0]*23,[0]*23]
    for i in range(1,max_id+1):
        answers = lst_all_grades[i-1]
        temp = good_answer(lst_answer,answers,histo)
        lst.append(temp+final_grade(temp,id_serie,lst_redac_grade[i-1]))
    return lst,histo

def print_grade(max_id,lst_answer,id_serie,lst_all_grades,lst_name,redac_grade):
    #lst_name = []
    lst_redac_grade = redac_grade
    '''for i in range(max_id):
        lst_name.append(input("Nom de l'eleve "+str(i+1)+": \n"))
        lst_redac_grade.append(int(input("Note de "+lst_name[i]+"\n")))'''
    grade_all_students,histo = all_student(lst_answer,max_id,id_serie,lst_redac_grade,lst_all_grades)
    for i in range(max_id):
        print("Note de "+lst_name[i])
        for j in range(8):
            print("\tSerie "+str(j+1)+" : "+str(grade_all_students[i][j][0])+"/"+str(grade_all_students[i][j][1]))
        print("\tNote de Francais: "+str(grade_all_students[i][8]))
        print("\tNote de Math: " + str(grade_all_students[i][9]))
        print("\tNote d'Anglais: " + str(grade_all_students[i][10]))
        print("\tNote Final: " + str(grade_all_students[i][11]))
        print("\n")

def print_grade_up(max_id,lst_answer,id_serie,lst_all_grades,lst_name,redac_grade):
    #lst_name = []
    lst_redac_grade = redac_grade
    grade_all_students,histo = all_student(lst_answer,max_id,id_serie,lst_redac_grade,lst_all_grades)
    for i in range(max_id):
        print(lst_name[i]+";"+str(grade_all_students[i][8])+";"+str(grade_all_students[i][9])+";"+str(grade_all_students[i][10])+";"+str(grade_all_students[i][11]))


def print_histo_up(max_id,lst_answer,id_serie,lst_all_grades,lst_name,redac_grade):
    #lst_name = []
    lst_redac_grade = redac_grade
    grade_all_students,histo = all_student(lst_answer,max_id,id_serie,lst_redac_grade,lst_all_grades)
    for count, i in enumerate(histo):
        names = [str(x) for x in range(1,len(i)+1)]
        values = i[:]
        plt.figure(figsize=(18, 6))
        plt.bar(names, values)
        plt.plot(names, values)
        plt.suptitle(f"Serie : {count+1}")
        string = "Serie "+str(count+1)+".png"
        plt.savefig(string)

def print_verif(max_id):
    for i in range(1, max_id + 1):
        name = input()
        print(f"{name}")
        if i < 10:
            image = Image.open('000' + str(i) + '.jpg')
        else:
            image = Image.open('00' + str(i) + '.jpg')
        image_rgb = image.convert("RGB")
        for j in lst_answer_exam(image_rgb):
            print(" ".join(j))
        print(10)

def get_lst(max_id):
    lst_grade, lst_name, redac_grade = [], [],[]
    for i in range(max_id):
        lst_name.append(input())
        lst_grade.append([])
        for j in range(8):
            temp = input()
            lst_grade[i].append([int(x) for x in temp.split(" ")])
        redac_grade.append(int(input()))
    return lst_grade,lst_name,redac_grade

lst_answer = [[3,4,4,1,4,2,1,2,3,4,2,2,2,3,3,2,2,2,3,3,5],[2,3,3,2,1,1,3,2,1,2,2,3,2,4,3,4,3,2,1,4],[2,2,1,2,1,1,4,4,2,3,3,2,3,2,2,3,4,2,1,4,5],[3,3,1,3,2,2,3,1,2,1,3,1,3,4,4,4,4,1,3,4],[4,2,4,3,1,1,4,1,4,4,2,2,1,2,3,3,4,2,2,4,2,1,5],[1,2,2,4,4,2,4,1,2,2,1,3,3,2,4,3,1,4,1,4,2,1],[4,3,2,1,2,1,2,1,1,1,1,3,4,1,4,2,3,1,1],[3,2,4,4,2,1,1,4,3,2,3,3,3,1,4,3,4,4,4,1,2,4]]


## id serie : 1--> Francais, 2--> Math, 3-->Anglais

id_serie = [[1,2],[3,4],[5,6]]


max_id = 24


####Analyser les Donner

lst_all_grades,lst_name,redac_grade = get_lst(max_id)
print_grade_up(max_id,lst_answer,id_serie,lst_all_grades,lst_name,redac_grade)


#print_histo_up(max_id,lst_answer,id_serie,lst_all_grades,lst_name,redac_grade)


###Recuperer donner depuis images
#print_verif(max_id)





'''image = Image.open("0019.jpg")
image_rgb = image.convert("RGB")
print(first_pixel(image_rgb))'''
#print(lst_answer_exam(image_rgb))
#final_grade(lst,lst)
