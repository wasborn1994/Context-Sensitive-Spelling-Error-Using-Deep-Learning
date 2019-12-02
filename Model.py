from Utility import Pre_Utility
from Pre_start import Pre_Start
import pdb
import time

token_Pre_Utility=Pre_Utility()
token_Pre_Start=Pre_Start()
sentence=''
prob_sentence=[]
Me=[]
order_list=[]
pivot_list=[]
switch_bit=0
error_check_list=[]

JOSA_LIST_one=["은","는","의","을","과","에","나","서","이","로","를","다","가","도","할","함",
"와","마","럼","터","만","게","란","아","차"
,"지","고","께","두","뿐","루","저","야","랑","써"
,"요","큼","테","라","녕"
,"냥","러","치","여","담"
,"며","면"] 

JOSA_LIST_two=["이나","에서","으로","나마","처럼","부터","에게","부터","이란","조차"
,"마다","보다","까지","대로","로서","하고","에다","에도","보고",
"말로","마저","이야","부터","로서","께서","다가","밖에","로써"
,"게서","만큼","치고","같이","로써","나마","말로","한테","따라","테서","커녕"
,"다가","커녕","따나","부터","마냥","더러","만치","깨나","이서","시여","보담"
,"일랑","으루","커녕","께서","테만","부터","까지","마저","따라","처럼","만큼",
           "이며","더러","으로","하고","하며","조차","에서","께서",
           "에게","보다","이고","들을","이면","것도","들이","님이","해요","이다"] 

out = open("output2.txt", 'w')
oov = open("oov.txt", 'w')
JOSA_LIST=["은","는","의","을","과","에","이나","에서","이","으로","를","다","로","가","도","할","함",
"와","이나마","서","처럼","부터","만","에게","로부터","으로부터","이란","아","조차"
,"나","마다","보다","까지","대로","로서","하고","께","두","에다","에도","보고","뿐","루"
"야말로","마저","이야","야","에서부터","으로서","란","께서","다가","랑","밖에","으로써"
,"요","에게서","만큼","치고","같이","로써","나마","이야말로","한테","따라","한테서","은커녕"
,"에다가","는커녕","마따나","서부터","마냥","더러","만치","깨나","이서","이시여","보담"
,"일랑","으루","커녕","께서","한테만","부터","까지","마저","따라","처럼","만큼",
           "이며","더러","으로","하고","하며","조차","에서","께서",
           "에게","보다","이고","들을","이면","것도","들이","님이","해요","이다"] 
dic_name="ㄱㄴㄷㄹㅁㅂㅅㅇㅈㅊㅋㅌㅍㅎ"
class Pre_Spacing:
    
    error_sentence_list=[]

    def window_logprob(self,ngram,Prob_list):
        ngram=str(ngram)
        if ngram in Prob_list:
            return Prob_list[ngram]
        else:
            return 0
    def window(self,sent,Prob_list):
        sent_logprob=self.window_logprob(sent,Prob_list)
        return sent_logprob
    def Pre_process_02_01_Spacing_Main(self,error_list,JaMo_list,Prob_list,Noun_list):
        global sentence
        global prob_sentence
        sentence=''
        prob_sentence=[]
        space_count=0
        original_list=error_list[0]
        modify_list=error_list[1]
        index_list=error_list[2]
        for i in range(len(original_list)):
            if i in index_list:
                self.error_sentence_list=self.Pre_process_02_02_Spacing_Words(self.error_sentence_list,space_count,original_list[i],i,modify_list,JaMo_list,Prob_list,Noun_list)
            else:
                if len(original_list)==1 and i==0:
                    sentence+=original_list[i]
                    string_l=len(original_list[i])
                    temp2_word=original_list[i]
                    out.write(temp2_word)
                else:
                    if (len(original_list)-1)==i:
                        sentence+=' '+original_list[i]
                        prob_sentence.append('3136')
                        string_l=len(original_list[i])
                        temp2_word=original_list[i]
                        out.write(temp2_word)
                    else:
                        sentence+=' '+original_list[i]
                        prob_sentence.append('3136')
                        out.write(original_list[i])

            space_count+=1
        return sentence
    def Pre_process_02_02_Spacing_Words(self,error_s_list,space_count,eojeol,position,right_list,JaMo_list,Prob_list,Noun_list):
        index_arr=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        global sentence
        global prob_sentence
        global switch_bit
        self.error_sentence_list=error_s_list
        max_eojeol=len(eojeol)
        index_number=0
        if max_eojeol>5:
            prob_sentence.append(eojeol)
            if space_count==0:
                out.write(eojeol)
            else:
                out.write(' '+eojeol)
            sentence+=' '+eojeol
            return self.error_sentence_list
        suggestions_temp=[]
        suggestions=[]
        keyword=[]
        king=0
        switch=0
        string_temp=''
        original_text=''
        answer_word=''
        if eojeol!=right_list[position]:
            prob_sentence.append(eojeol)
            if space_count==0:
                out.write(eojeol)
            else:
                out.write(' '+eojeol)
            sentence+=' '+eojeol
            return self.error_sentence_list
        keyword=temp_word=token_Pre_Utility.Pre_process_02_04_Korean_Lettering_Divide(eojeol)
        if temp_word!=[]:
            temp_word.pop()
            sin=dic_name.find(temp_word[0])
            cos=self.Pre_process_02_03_Dic_Slection(sin,JaMo_list)
            if True==cos.find(temp_word):
                prob_sentence.append(eojeol)
                if space_count==0:
                    out.write(eojeol)
                else:
                    out.write(' '+eojeol)
                sentence+=' '+eojeol
                return self.error_sentence_list
            elif max_eojeol>2:
                #이부분 응급처치
                if eojeol[max_eojeol-1] in JOSA_LIST_one:
                    temp_bacuni=token_Pre_Utility.Pre_process_02_04_Korean_Lettering_Divide(eojeol[:max_eojeol-1])
                    temp_bacuni.pop()
                    sin=dic_name.find(temp_bacuni[0])
                    cos=self.Pre_process_02_03_Dic_Slection(sin,JaMo_list)
                    if True==cos.find(temp_bacuni):
                        prob_sentence.append(eojeol[:max_eojeol-1])
                        if space_count==0:
                            out.write(eojeol)
                        else:
                            out.write(' '+eojeol)
                        sentence+=' '+eojeol
                        return self.error_sentence_list
                    else: 
                        if eojeol[max_eojeol-2:max_eojeol] in JOSA_LIST_two:
                            temp_bacuni=token_Pre_Utility.Pre_process_02_04_Korean_Lettering_Divide(eojeol[:max_eojeol-2])
                            temp_bacuni.pop()
                            sin=dic_name.find(temp_bacuni[0])
                            cos=self.Pre_process_02_03_Dic_Slection(sin,JaMo_list)
                            if True==cos.find(temp_bacuni):
                                prob_sentence.append(eojeol[:max_eojeol-2])
                                if space_count==0:
                                    out.write(eojeol)
                                else:
                                    out.write(' '+eojeol)
                                sentence+=' '+eojeol
                                return self.error_sentence_list
                suggestions_temp=token_Pre_Start.suggest_words(cos,temp_word,1)
                if suggestions_temp!=[]:
                    suggestions=suggestions_temp
                else:
                    prob_sentence.append(eojeol)
                    if space_count==0:
                        out.write(eojeol)
                    else:
                        out.write(' '+eojeol)
                    sentence+=' '+eojeol
                    return self.error_sentence_list
            else:
                prob_sentence.append(eojeol)
                if space_count==0:
                    out.write(eojeol)
                else:
                    out.write(' '+eojeol)
                sentence+=' '+eojeol
                return self.error_sentence_list
        else:
            prob_sentence.append(eojeol)
            if space_count==0:
                out.write(eojeol)
            else:
                out.write(' '+eojeol)
            sentence+=' '+eojeol
            return self.error_sentence_list


            #return eojeol
        #여기에서 잘라내는연산    

        if suggestions!=[] and keyword!=[]:
            master=keyword[0]
            sug=[]
            goal=suggestions
            for temp in goal:
                if master==temp[0][0]:
                    temp2 = [x for x in temp[0]]
                    sug.append(temp2)
            #print("오류단어입니다:",keyword)
            #print("교정단어후보들입니다.",sug)
            #answer_word=Pre_process_03_01_Typo_and_Dic_Compare(keyword,sug)
            #print("최종후보입니다.",answer_word)
            #    여기에 확률 메카니즘start
            if len(sug)!=1 and len(sug)<=2:
                candidate_count=len(sug)
                candidate_list=[]
                candidate_compare_list=[]
                candidate_answer_list_temp=[]
                candidate_answer_list=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                #후보 많으면 그냥 룰 기반 
                max_pivot=0
                max_index=-1
                min_pivot=0
                final_answer=-1
                for i in range(candidate_count):
                    candidate_list.append(token_Pre_Utility.Pre_process_03_02_Korean_Lettering_Combine(sug[i]))
                temp_max_index=len(right_list)

                for j in range(candidate_count):
                    list1=[]
                    for i in range(position-3,position+4):
                        if position==i or i<0 or i>=temp_max_index:
                            continue
                        if i<position:
                            list1.append(self.window((prob_sentence[i],candidate_list[j]),Prob_list))
                            if min_pivot>list1[-1]:
                                min_pivot=list1[-1]
                        else:
                            list1.append(self.window((candidate_list[j],right_list[i]),Prob_list))
                            if min_pivot>list1[-1]:
                                min_pivot=list1[-1]
                    candidate_compare_list.append(list1)
                if min_pivot!=0:
                    min_pivot=(-min_pivot)+1

                    for i in range(candidate_count):

                        for j in range(len(candidate_compare_list[i])):
                            if candidate_compare_list[i][j]==0:
                                continue
                            else: 
                                candidate_answer_list[i]+=candidate_compare_list[i][j]+min_pivot
                    for i in range(candidate_count):
                        if max_pivot<candidate_answer_list[i]:
                            max_pivot=candidate_answer_list[i]
                            max_index=i


                    if max_index==-1:
                        answer_word=token_Pre_Utility.Pre_process_03_02_Korean_Lettering_Combine(keyword)
                    else:
                        answer_word=candidate_list[max_index]
                else:
                    answer_word=answer_word=token_Pre_Utility.Pre_process_03_02_Korean_Lettering_Combine(keyword)
            elif len(sug)>5:
                answer_word=token_Pre_Utility.Pre_process_03_02_Korean_Lettering_Combine(keyword) 
            elif len(sug)==1:
                answer_word=token_Pre_Utility.Pre_process_03_02_Korean_Lettering_Combine(sug[0])
            # 확률 메카니즘 end
            answer_word_temp_bacuni=''
            if eojeol[index_number:] in JOSA_LIST:
                prob_sentence.append(answer_word)
                answer_word+=eojeol[index_number:]
                if space_count==0:
                    out.write(answer_word)
                else:
                    out.write(' '+answer_word)
                if answer_word!=eojeol:
                    self.error_sentence_list.append(space_count)
                    #pdb.set_trace()
                    

                sentence+=' '+answer_word    
            else:
                if space_count==0:
                    out.write(answer_word)
                else:
                    out.write(' '+answer_word)
                if answer_word!=eojeol:
                    self.error_sentence_list.append(space_count)
                sentence+=' '+answer_word
                prob_sentence.append(answer_word)
        elif suggestions==[]:
            if space_count==0:
                out.write(eojeol)
            else:
                out.write(' '+eojeol)
            sentence+=' '+eojeol
            prob_sentence.append(eojeol)
        return self.error_sentence_list


    def Pre_process_02_03_Dic_Slection(self,sin,Dict_list):
        if sin==0:
            return Dict_list[0]
        elif sin==1:
            return Dict_list[1]
        elif sin==2:
            return Dict_list[2]
        elif sin==3:
            return Dict_list[3]
        elif sin==4:
            return Dict_list[4]
        elif sin==5:
            return Dict_list[5]
        elif sin==6:
            return Dict_list[6]
        elif sin==7:
            return Dict_list[7]
        elif sin==8:
            return Dict_list[8]
        elif sin==9:
            return Dict_list[9]
        elif sin==10:
            return Dict_list[10]
        elif sin==11:
            return Dict_list[11]
        elif sin==12:
            return Dict_list[12]
        elif sin==13:
            return Dict_list[13]
        elif sin==-1:
            return Dict_list[14]
    
