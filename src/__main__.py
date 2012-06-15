
def get_input(path):
    f = open(path, 'r')
    string = f.readlines()
    data_set = []
    row = 0
    
    for line in string:
        data = line.split('\t')
        data_set.append([])
        
        data_set[row].append(float(data[0])/2400)
        data_set[row].append(float(data[1])/900)
        data_set[row].append(float(data[2])/300)
        data_set[row].append(int(data[3]))
                    
        row += 1
        
    f.close()
    
    return data_set

def define_patterns(som, data_set):
    pattern0 = [[0 for j in range(len(som.neurons[i]))] for i in range(len(som.neurons))]
    pattern1 = [[0 for j in range(len(som.neurons[i]))] for i in range(len(som.neurons))]
    
    for row in data_set:
        winner = som.find_winner(row)
        
        if row[-1] == 0:
            pattern0[winner.row][winner.column] += 1
        else:
            pattern1[winner.row][winner.column] += 1
                
    for i in range(len(som.neurons)):
        for j in range(len(som.neurons[i])):
            if pattern0[i][j] == 0 and pattern1[i][j] == 0:
                som.neurons[i][j].recognized_pattern = None
            else:
                if pattern0[i][j] > pattern1[i][j]:
                    som.neurons[i][j].recognized_pattern = 0
                else:
                    som.neurons[i][j].recognized_pattern = 1
#            if som.neurons[i][j].recognized_pattern == None:
#                print 'N ',
#            else:
#                print str(som.neurons[i][j].recognized_pattern) + ' ',
#        print '\n'


if __name__ == '__main__':
    from kohonen.KohonenNetwork import Kohonen
    
    training_set = get_input('../datasets/training_set2.txt')
    test_set = get_input('../datasets/test_set.txt')
    
    string = raw_input().split(' ')
    
    rows = int(string[0])
    cols = int(string[1])
    l_rate = float(string[2])
    e_w = float(string[3])
    t = int(string[4])

    
    total_c = 0
    total_nc = 0
  
    for data in test_set:
        if data[-1] == 0:
            total_c += 1
        else:
            total_nc += 1

    
    while rows != 0 and cols != 0 and l_rate != 0.0 and e_w != 0.0 and t != 0:
        cont_c = 0
        cont_nc = 0

        k = Kohonen(3, rows, cols, l_rate, e_w)

        k.learn(t, training_set, define_patterns)
    
        cont_hit = 0
        
        for test_data in test_set:
            answer = k.test(test_data)
        
            if answer == test_data[-1]:
                cont_hit += 1
            
                if test_data[-1] == 0:
                    cont_c += 1
                else:
                    cont_nc += 1

    
        hit_rate = (float(cont_hit) * 100) / float(len(test_set))
        c_rate = (float(cont_c) * 100) / float(total_c)
        nc_rate = (float(cont_nc) * 100) / float(total_nc)
        
        print 'O acerto para confinado foi: ' + str(c_rate)
        print 'O acerto para nao confinado foi: ' + str(nc_rate)
        print 'O acerto total da RNA foi: ' + str(hit_rate) + '\n\n\n'
        
        string = raw_input().split(' ')
    
        rows = int(string[0])
        cols = int(string[1])
        l_rate = float(string[2])
        e_w = float(string[3])
        t = int(string[4])