% from template_utils import *
% rebase('base.tpl', title='Urban Kombat')

<table width="100%">
    <tr>
        <td class="cp">
            <table class="c" cellspacing=0>
                <tr>
                    <td colspan=3 class="sb">Roftwood</td>
                </tr>
                <tr>
                    <td class="b c9">
                        <input type="button" class="mr" value="Eligius General Hospital">
                    </td>
                    <td class="b c33">
                        <input type="button" class="md" value="Turpin Crescent">
                    </td>
                    <td class="b c3">
                        <input type="button" class="md" value="a carpark">
                    </td>
                </tr>
                <tr>
                    <td class="b c33">
                        <input type="button" class="md" value="Purchas Alley">
                    </td>
                    <td class="b cx">
                        <input type="button" class="ml" value="Hildebrand Mall">
                    %if len(humans) > 0:
                        <br>
                        %for player in humans[:3]:
                            <a href="#" class="f1">{{player.name}}</a>   
                        %end
                    %end
                    %if len(zombies) > 0:
                        <br>
                        <span class="fz">{{len(zombies)}} zombie\\
%if len(zombies) > 1:
s</span>
%end
                    %end
                    </td>             
                    <td class="b cx">
                        <input type="button" class="ml" value="Hildebrand Mall">
                        <br>
                        <a href="#" class="f1 con4">javboy</a>
                    </td>
                </tr>
                <tr>
                    <td class="b c0">
                        <input type="button" class="md" value="Sloper Row">
                    </td>
                    <td class="b cx">
                        <input type="button" class="ml" value="Hildebrand Mall">
                        <br>
                        <a href="#" class="f1 con5">doofus217</a> <a href="profile.cgi?id=218759" class="f3">pablazo</a>
                    </td>
                    <td class="b cx">
                        <input type="button" class="ml" value="Hildebrand Mall">
                        <br>
                        <a href="#" class="f1">Indiana&nbsp;Jone</a>
                        <a href="#" class="f2 con5">Doc&nbsp;Spalding</a>
                        <a href="#" class="f3">Weside4lyfe</a>
                    </td>
                </tr>
            </table>
            <div class="gt">You are <a href="#"><b>{{name}}</b></a>\\
%if dead:
 and you are <b>dead</b>\\
%end
. You have <b>{{health}}</b> Hit
                Points and <b>9678</b> Experience Points. <span class="{{'ap' if ap > 5 else 'apw'}}">You have <b>{{ap}}</b> Action Points
                    remaining.</span></div>
            <div class="gthome">Your safehouse is <b>the Blackmore Building</b>, 11 blocks west and 8 north. 
                <div class="a formlike"><input class="m" value="Set here" type="button"></div>
            </div>
            <p>
                <a href="#" class="y">Buy skills</a>
                <a href="#" class="y">Contacts</a>
                <a href="#" class="y">Settings</a>
                <a href="#" class="y">Log out</a>
            </p>
            <p>
                <a href="#" class="y">News</a>
                <a href="#" class="y">FAQ</a>
                <a href="#" class="y">Wiki</a>
                <a href="#" class="y">Donate</a>
            </p>
        </td>
        <td class="gp">
            <div class="gt">You are inside <b>Hildebrand Mall</b>. Trails of looted debris litter the floors and
                escalators. The building has been quite strongly barricaded. \\
%if len(humans) > 0:
Also here is              
%for last,player in detect_last(humans):
<a href="#" class="\\
%if player.team == team:
con5\\
%else:
con2\\
%end
">{{player.name}}</a> \\
    %if player.health != 60:
<span class="trg">\\
    %end
({{player.health}}<sub>HP</sub>)\\
    %if player.health != 60:
</span>\\
    %end
    %if not last:
, \\
    %else:
.\\
    %end
%end
%end
<br><br>A portable generator has been set up here. It is running.
                <br><br>Somebody has spraypainted <i>death to fascism, freedom to the people</i> onto a wall.\\
                %if len(zombies) > 0:
<br><br>\\
    %include("zombies.tpl")
%end
</div>\\
%if len(since_last_turn) > 0:
<p><b>Since your last turn:</b></p><ul>\\
    %for event in since_last_turn:
<li>{{event}}</li>\\
    %end
%end
</ul>
%if defined("message"):
<p></p><p class="gamemessage"><b>{{message}}</b></p>
%end

            <p>Possible actions:</p>
            <div class="a formlike"><input class="m" type="button" value="Leave Hildebrand Mall"></div>
            <div class="a formlike"><input class="m" type="button" value="Barricade the building"></div>
            <div class="a formlike"><input type="button" class="m" value="Search the Gun Store"></div>
            <div class="a formlike"><input type="button" class="m" value="Search the Tech Store"></div>
            <div class="a formlike"><input type="button" class="m" value="Search the Hardware Store"></div>
            <div class="a formlike"><input type="button" class="m" value="Search the Sports Store"></div>
            <div class="a formlike"><input type="button" class="m" value="Search the Liquor Store"></div>
            <div class="a formlike"><input type="button" class="m" value="Search the Bookstore"></div>
            <div class="a formlike"><input type="button" class="m" value="Search the Drugstore"></div><br>

            <form action="map.cgi" method="post" class="a">
                <input type="submit" value="Attack" class="m">&nbsp;\\
%include("target.tpl")
&nbsp;with&nbsp;<select name="weapon">
%for attack in attacks:
                    <option value="{{attack.action}}" {{"selected" if defined("last_weapon") and attack.action == last_weapon else ""}}> {{attack.name}} ({{attack.chance}}%, {{attack.damage}} dam)</option>
%end
                </select>
            </form>

%if not defined("inventory"):
<p>As a zombie, you are unable to use the objects you are carrying.</p>
%else:
            <p>Inventory (click to use):</p>

    %for item in inventory:                      
            <form action="map.cgi?{{item.action}}" method="post" class="a"><input type="submit" value="{{item.name}}" class="m">\\
%if hasattr(item, "shots"):
({{item.shots}})\\
%end
<%
if item.target and (len(humans) > 0 or len(zombies) > 0):
    include("target.tpl", include_self=True)
end
%>
</form>
    %end
        </td>
    </tr>
</table>