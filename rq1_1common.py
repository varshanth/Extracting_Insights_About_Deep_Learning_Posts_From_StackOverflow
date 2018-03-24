################### RQ1.1 COMMON DATA STRUCTS #################################

# Order Matters! => Designations are matched in the order that they appear
_designations = [
        'Academia-Professional',
        'Professional',
        'Academia-Ambiguous',
        'Academia-Pedagogical',
        'Academia-Student',
        'Professional-Ambiguous',
        'Online-User-Profile-Present'
        ]


_designation_map = {
        'Academia-Student' : {
                'student', 'freshman','sophomore', 'grad', 'b.e ', 'mtech',
                'bachelor', 'phd', 'ph.d', 'school', 'studying', 'thesis',
                'academic', 'college', 'teaching assistant', 'university',
                'data science', 'computer science', 'intern', 'msc', 'postdoc',
                'engineering', 'research', 'masters', 'btech'
                },
        'Academia-Pedagogical' : {
                'professor', 'lecturer', 'teacher', 'teach'
                },
        'Academia-Ambiguous' : {
                'researcher', 'computer scientist', 'mathematician',
                'bioinformatician', 'statistician', 'physicist',
                'neuroscientist', 'biologist', 'scientist'
                },
        'Academia-Professional' : {
                'research engineer', 'data scientist', 'research scientist',
                'machine learning engineer'
                },
        'Professional' : {
                'developer', 'engineer ', 'designer', 'analyst', 'contractor',
                'software engineer', 'software developer', 'data engineer',
                'graphic designer', 'cs engineer', 'computer engineer',
                'consultant', 'architect', 'manager', 'development',
                'professional', 'founder', 'leader', 'team lead', 'tech lead',
                'technical leader', 'work on', 'dev', 'freelance', 'work at',
                'company', 'engineer,', 'engineer.', 'engineer<', 'specialist',
                'startup'
                },
        'Online-User-Profile-Present' : {
                'http', 'www'
                },
        'Professional-Ambiguous' : {
                'programmer', 'coder'
                }
        }
###############################################################################