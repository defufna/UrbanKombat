%import importlib
%import template_utils
%importlib.reload(template_utils)
% from template_utils import *
% zombie_count = len(zombies)
%if zombie_count == 1:
    %if is_zombie:
There is another zombie here.
    %else:
There is a lone zombie here.    
    %end
%elif zombie_count > 1:
There {{collective_phrase(zombie_count)}} {{count(zombie_count)}}\\
%if is_zombie:
other\\
%end
 zombies here\\
%if is_zombie:
{{count(same_team_zombies)}} of them from your horde\\
%end
.
You recognise \\
%for last, player in detect_last(zombies):
<a href="#" class="\\
%if player.team == team:
con5\\
%else:
con2\\
%end
">{{player.name}}</a>\\
    %if not last:
, \\
    %else:
.\\
    %end
%end

%end