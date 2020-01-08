#!/bin/python3

basefile = './endRound.csv'
file2 = './leth_mob_infec_dur.csv'
file3 = './leth_mob_infec_dur_quarantine_only.csv' 

file_arr = [basefile,file2,file3]


def analyse() :
	
	data_arr = {}
	
	for path in file_arr :
		cur_file_data_arr = {} 
		with open( path , 'r' ) as fh :
			line = fh.readline().split(',')	
			line = fh.readline().split(',')
			while line and line != [''] :
				# first ist rounds , second is win ? 
				cur_file_data_arr[line[0]] = [int ( line[2] ) , line[3] == 'win\n' ]
				
				line = fh.readline().split(',')		
		data_arr[path] = cur_file_data_arr 

	data_lenth = len( data_arr[ basefile ] ) 
	
	eval_arr = {}
	for key in data_arr.keys() :
		win_ctr = 0
		round_ctr = 0
		more_rounds = 0
		less_rounds = 0
		diff_wins_more = 0
		diff_wins_less = 0
		wins_equal = 0
		loss_equal = 0
		for data in data_arr[key] :
			cur_data = data_arr[key][data]  
			if cur_data[1] :
				win_ctr += 1 
			round_ctr += cur_data[0]
			if key != basefile :
				cur_diff_round = data_arr[key][data][0] - data_arr[basefile][data][0]
				if cur_diff_round > 0 :
					more_rounds += cur_diff_round
				else:
					less_rounds -= cur_diff_round
				
				if data_arr[basefile][data][1] and not cur_data[1] :
					diff_wins_less += 1
				elif not data_arr[basefile][data][1] and cur_data[1] :
					diff_wins_more += 1
				elif not data_arr[basefile][data][1] and not cur_data[1] :
					loss_equal += 1
				else :
					wins_equal += 1
		if key != basefile :
			print( f'{key} analysis compared to endRound\n needed more rounds : {more_rounds}\nneeded less rounds {less_rounds}\ngames where won too { wins_equal},\nlost too {loss_equal}\n lost instead of won {diff_wins_less}\n won instead of lost {diff_wins_more}' )

				
		eval_arr[key] = [ win_ctr , round_ctr ]
				
	print( eval_arr ) 	 

if __name__ == "__main__" :
	analyse() 
	


