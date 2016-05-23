__author__ = 'WSY'
import sys
import string
import math

def F_score(predict_path, base_path):

    f_predict = open(predict_path, 'r')
    f_base = open(base_path, 'r')
    pre_content = f_predict.read().strip().split('\n')
    base_content = f_base.read().strip().split('\n')
    pre_content.append('')
    base_content.append('')

    if(len(pre_content) != len(base_content)):
        error_info = "length of predictFile is not equal with length of baseFile"
        print error_info
        sys.exit()

    k = 0
    sigma = []
    fai = []
    pre_name = pre_content[0].split(',')[0]
    i = 0
    sigma_sum = 0
    fai_sum = 0
    sigma_val = 0
    fai_val = 0

    for i in range(len(pre_content)):
        cur_predict_name = pre_content[i].split(',')[0]
        cur_base_name = base_content[i].split(',')[0]
        #print pre_name, cur_predict_name

        if pre_name == cur_predict_name:
            if cur_predict_name == cur_base_name:
                s = string.atof(pre_content[i].split(',')[1])
                t = string.atof(base_content[i].split(',')[1])
                #print s, t
                k += 1
                sigma_sum += math.pow((s-t)/t, 2)
                fai_sum += t
            else:
                print "predict_name is not equal base_name"
                sys.exit()
            pre_name = cur_predict_name

        else:
            sigma_val = math.sqrt(sigma_sum/k)
            fai_val = math.sqrt(fai_sum)
            print ("N = %d, Sigma = %f, Fai = %f" % (k, sigma_val, fai_val))
            sigma.append(sigma_val)
            fai.append(fai_val)

            pre_name = cur_predict_name
            sigma_sum = 0
            fai_sum = 0
            k = 0

            if len(cur_predict_name) > 0:
                if cur_predict_name == cur_base_name:
                    s = string.atof(pre_content[i].split(',')[1])
                    t = string.atof(base_content[i].split(',')[1])
                    #print s, t
                    k += 1
                    sigma_sum += math.pow((s-t)/t, 2)
                    fai_sum += t
                else:
                    print "predict_name is not equal base_name"
                    sys.exit()

    #print len(sigma), len(fai)
    #print sigma
    #print fai

    f_score = 0
    for i in range(len(sigma)):
        f_score += (1 - sigma[i])*fai[i]

    print ("F_Score = %f" % f_score)
    return f_score


if __name__ == '__main__':
    #F_score("predict.csv", "base.csv")
    F_score("data2\mars_tianchi_artist_plays_predict.csv", "data2\mars_tianchi_artist_plays_predict.csv")
