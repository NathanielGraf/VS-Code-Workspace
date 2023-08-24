'''
Our new contest submission system keeps a chronological log of all submissions made by each team during the contest. With each entry, it records the number of minutes into the competition at which the submission was received, the letter that identifies the relevant contest problem, and the result of testing the submission (designated for the sake of this problem simply as right or wrong). As an example, the following is a hypothetical log for a particular team:

3 E right
10 A wrong
30 C wrong
50 B wrong
100 A wrong
200 A right
250 C wrong
300 D right
The rank of a team relative to others is determined by a primary and secondary scoring measure calculated from the submission data. The primary measure is the number of problems that were solved. The secondary measure is based on a combination of time and penalties. Specifically, a team’s time score is equal to the sum of those submission times that resulted in right answers, plus a 20-minute penalty for each wrong submission of a problem that is ultimately solved. If no problems are solved, the time measure is 
.

In the above example, we see that this team successfully completed three problems: E on their first attempt (
 minutes into the contest); A on their third attempt at that problem (
 minutes into the contest); and D on their first attempt at that problem (
 minutes into the contest). This teams time score (including penalties) is 
. This is computed to include 
 minutes for solving E, 
 minutes for solving A with an additional 
 penalty minutes for two earlier mistakes on that problem, and finally 
 minutes for solving D. Note that the team also attempted problems B and C, but were never successful in solving those problems, and thus received no penalties for those attempts.

According to contest rules, after a team solves a particular problem, any further submissions of the same problem are ignored (and thus omitted from the log). Because times are discretized to whole minutes, there may be more than one submission showing the same number of minutes. In particular there could be more than one submission of the same problem in the same minute, but they are chronological, so only the last entry could possibly be correct. As a second example, consider the following submission log:

7 H right
15 B wrong
30 E wrong
35 E right
80 B wrong
80 B right
100 D wrong
100 C wrong
300 C right
300 D wrong
This team solved 4 problems, and their total time score (including penalties) is 
, with 
 minutes for H, 
 for E, 
 for B, and 
 for C.

Input
The input contains 
 lines for 
, with each line describing a particular log entry. A log entry has three parts: an integer 
, with 
, designating the number of minutes at which a submission was received, an uppercase letter designating the problem, and either the word right or wrong. The integers will be in nondecreasing order and may contain repeats. After all the log entries is a line containing just the number 
.

Output
Output two integers on a single line: the number of problems solved and the total time measure (including penalties).


'''
    
    

def main():
    
    #Find the score of the team
    #Find the number of problems solved
    
        
            
        
    
    return 0

main()