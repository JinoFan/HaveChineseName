#!"D:\XAMPPfile\perl\bin\perl.exe"
use Encode;
use utf8;

print "Content-type: text/html;charset=utf-8\n\n";
read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
@data = split(/&/, $buffer);
foreach (@data){
   ($key, $value) = split(/=/);
   $value =~ tr/+/ /;
   $value =~ s/%(..)/pack("C", hex($1))/eg;
   $info{$key} = $value;
}

if($info{'style'} eq 'transliterated'){
	transliterated($info{'name'});
}
if($info{'style'} eq 'artistic'){
	artistic($info{'gender'});
}
if($info{'style'} eq 'thoeretical'){
	thoeretical($info{'year'},$info{'month'},$info{'date'},$info{'hour'});
}

sub transliterated(){
	open(In,"Chara.gb");
	while(<In>){
		chomp;
		if(/(\S+) (\S+)/){
			push(@arrayHZ,$1);
			@arrayPY=split("",$2);
			$HashYinZi{$1}=$arrayPY[0];
		}
	}
	close(In);

	open(In,"HSK.txt");
	while(<In>){
		chomp;
		if(/(\S+) (.+)/){
			$HashHSK{$1}=$2;
		}
	}
	close(In);
	
	open(In,"firstname.txt");
	while(<In>){
		chomp;
		push(@firstname,$_);
	}
	close(In);

	my ($MyName)=@_;
	@arrayName=split(" ",$MyName);
	for($i=0;$i<@arrayName;$i++){
		$arrayChar=substr($arrayName[$i],0,1);
		foreach $HZ(@arrayHZ){
			if ($HashYinZi{$HZ} eq lc($arrayChar)){
				if(($HashHSK{$HZ}=~/[ey]/)==0){
					push(@{$GetHZ[$i]},$HZ);
				}
			}
		}
	}
	for($i=0;$i<5;$i++){
		@Name=();
		for($j=0;$j<@arrayName;$j++){
			$refArray=$GetHZ[$j];
			$Namesub=int(rand(@{$refArray}));
			push(@Name,${$refArray}[$Namesub]);
		}
		foreach(@Name){
			$namelist[$i].=$_;
		}
	}
	
	
	for($i=0;$i<5;$i++){
		$namelist[$i]=$firstname[int rand(@firstname)].$namelist[$i];
		$namelist[$i]=decode('gb2312',$namelist[$i]);
	}
}

sub artistic(){
	my($gender)=@_;
	if($gender eq 'male'){
		open(In,'malename.txt');
	}elsif($gender eq 'female'){
		open(In,'femalename.txt');
	}
	while(<In>){
		chomp;
		push(@lastname,$_);
	}
	close(In);
	open(In,"firstname.txt");
	while(<In>){
		chomp;
		push(@firstname,$_);
	}
	close(In);
	for($i=0;$i<5;$i++){
		$namelist[$i]=$firstname[int rand(@firstname)].$lastname[int rand(@lastname)];
		$namelist[$i]=decode('gb2312',$namelist[$i]);
	}
}

sub thoeretical(){
	my ($year,$month,$date,$hour)=@_;
	@monthnum=(31,28,31,30,31,30,31,31,30,31,30,31);
	$day=($year-1900)*365+int(($year-1900)/4);
	for($i=0;$i<$month-1;$i++){
		$day+=$monthnum[$i];
	}
	$day+=$date;
	$day-=30;
	if($year%4==0 and $month<3){$day--;}

	open(In,"data.txt");
	while(<In>){
		chomp;
		$line.=$_;
	}
	close(In);
	
	@data=split(",",$line);
	foreach $num(@data){
		$hex=substr($num,3,3);
		$dec=hex($hex);
		$bin=sprintf("%012b",$dec);
		$num1=$bin=~tr/1/1/;
		$Day+=29*12+$num1;
		if (substr($num,6,1) ne '0'){
			if(substr($num,2,1) eq '1'){
				$Day+=30;
			}else{
				$Day+=29;
			}
		}
		$count++;
		if($Day>=$day){
			$Year=$count+1899;
			last;
		}
		$memory=$Day;
	}
	$Day=$memory;
	$hex=substr($data[$count-1],3,3);
	$dec=hex($hex);
	$bin=sprintf("%012b",$dec);
	for($i=0;$i<12;$i++){
		if(substr($bin,$i,1) eq '1'){
			$Day+=30;
		}else{
			$Day+=29;
		}
		$Month++;
		if($Day>=$day){
			$Date=$day-$memory;
			last;
		}
		$memory=$Day;
		if($IsLunar!=1 and (substr($data[$count-1],6,1) ne '0')){
			if(($i+1==substr($data[$count-1],6,1)) or 
			($i==9 and substr($data[$count-1],6,1) eq 'a') or 
			($i==10 and substr($data[$count-1],6,1) eq 'b') or 
			($i==11 and substr($data[$count-1],6,1) eq 'c')){
				if(substr($data[$count-1],2,1 eq '1')){
					$Day+=30;
				}else{
					$Day+=29;
				}
			if($Day>=$day){
				$Date=$day-$memory;
				last;
			}
			$IsLunar=1;
			$memory=$Day;
			$i--;next;
			}
		}
	}
	my ($gold,$wood,$water,$fire,$soil)=();
	
	if($Year%10==4 or $Year%10==5){$wood++;}
	if($Year%10==6 or $Year%10==7){$fire++;}
	if($Year%10==8 or $Year%10==9){$soil++;}
	if($Year%10==0 or $Year%10==1){$gold++;}
	if($Year%10==2 or $Year%10==3){$water++;}
	
	if($Year%12==4 or $Year%12==3){$water++;}
	if($Year%12==5 or $Year%12==8 or $Year%12==11 or $Year%12==2){$soil++;}
	if($Year%12==6 or $Year%12==7){$wood++;}
	if($Year%12==9 or $Year%12==10){$fire++;}
	if($Year%12==0 or $Year%12==1){$gold++;}
	
	if($Year%10==4 or $Year%10==9){
		if($Month==1 or $Month==2 or $Month==11 or $Month==12){$fire++;}
		if($Month==3 or $Month==4){$soil++;}
		if($Month==5 or $Month==6){$gold++;}
		if($Month==7 or $Month==8){$water++;}
		if($Month==9 or $Month==10){$wood++;}
	}
	if($Year%10==5 or $Year%10==0){
		if($Month==1 or $Month==2 or $Month==11 or $Month==12){$soil++;}
		if($Month==3 or $Month==4){$gold++;}
		if($Month==5 or $Month==6){$water++;}
		if($Month==7 or $Month==8){$wood++;}
		if($Month==9 or $Month==10){$fire++;}
	}
	if($Year%10==4 or $Year%10==9){
		if($Month==1 or $Month==2 or $Month==11 or $Month==12){$gold++;}
		if($Month==3 or $Month==4){$water++;}
		if($Month==5 or $Month==6){$wood++;}
		if($Month==7 or $Month==8){$fire++;}
		if($Month==9 or $Month==10){$soil++;}
	}
	if($Year%10==4 or $Year%10==9){
		if($Month==1 or $Month==2 or $Month==11 or $Month==12){$water++;}
		if($Month==3 or $Month==4){$wood++;}
		if($Month==5 or $Month==6){$fire++;}
		if($Month==7 or $Month==8){$soil++;}
		if($Month==9 or $Month==10){$gold++;}
	}
	if($Year%10==4 or $Year%10==9){
		if($Month==1 or $Month==2 or $Month==11 or $Month==12){$wood++;}
		if($Month==3 or $Month==4){$fire++;}
		if($Month==5 or $Month==6){$soil++;}
		if($Month==7 or $Month==8){$gold++;}
		if($Month==9 or $Month==10){$water++;}
	}
	
	if($Month==1 or $Month==2){$wood++;}
	if($Month==3 or $Month==6 or $Month==9 or $Month==12){$soil++;}
	if($Month==4 or $Month==5){$fire++;}
	if($Month==7 or $Month==8){$gold++;}
	if($Month==10 or $Month==11){$water++;}
	
	if($day%10==0 or $day%10==1){$wood++;}
	if($day%10==2 or $day%10==3){$fire++;}
	if($day%10==4 or $day%10==5){$soil++;}
	if($day%10==6 or $day%10==7){$gold++;}
	if($day%10==8 or $day%10==9){$water++;}
	
	if($day%12==0 or $day%12==3 or $day%12==6 or $day%12==9){$soil++;}
	if($day%12==1 or $day%12==2){$fire++;}
	if($day%12==4 or $day%12==5){$gold++;}
	if($day%12==7 or $day%12==8){$water++;}
	if($day%12==10 or $day%12==11){$wood++;}
	
	if($day%10==0 or $day%10==5){
		if(($hour>=0 and $hour<=3) or ($hour>=20 and $hour<=23)){$wood++;}
		if($hour>=4 and $hour<=7){$fire++;}
		if($hour>=8 and $hour<=11){$soil++;}
		if($hour>=12 and $hour<=15){$gold++;}
		if($hour>=16 and $hour<=19){$water++;}
	}
	if($day%10==1 or $day%10==6){
		if(($hour>=0 and $hour<=3) or ($hour>=20 and $hour<=23)){$fire++;}
		if($hour>=4 and $hour<=7){$soil++;}
		if($hour>=8 and $hour<=11){$gold++;}
		if($hour>=12 and $hour<=15){$water++;}
		if($hour>=16 and $hour<=19){$wood++;}
	}
	if($day%10==2 or $day%10==7){
		if(($hour>=0 and $hour<=3) or ($hour>=20 and $hour<=23)){$soil++;}
		if($hour>=4 and $hour<=7){$gold++;}
		if($hour>=8 and $hour<=11){$water++;}
		if($hour>=12 and $hour<=15){$wood++;}
		if($hour>=16 and $hour<=19){$fire++;}
	}
	if($day%10==3 or $day%10==8){
		if(($hour>=0 and $hour<=3) or ($hour>=20 and $hour<=23)){$gold++;}
		if($hour>=4 and $hour<=7){$water++;}
		if($hour>=8 and $hour<=11){$wood++;}
		if($hour>=12 and $hour<=15){$fire++;}
		if($hour>=16 and $hour<=19){$soil++;}
	}
	if($day%10==4 or $day%10==9){
		if(($hour>=0 and $hour<=3) or ($hour>=20 and $hour<=23)){$water++;}
		if($hour>=4 and $hour<=7){$wood++;}
		if($hour>=8 and $hour<=11){$fire++;}
		if($hour>=12 and $hour<=15){$soil++;}
		if($hour>=16 and $hour<=19){$gold++;}
	}
	
	if(($hour>=0 and $hour<=1) or ($hour>=22 and $hour<=23)){$water++;}
	if(($hour>=2 and $hour<=3) or ($hour>=8 and $hour<=9)
		or ($hour>=14 and $hour<=15) or ($hour>=20 and $hour<=21)){$soil++;}
	if($hour>=4 and $hour<=7){$wood++;}
	if($hour>=10 and $hour<=13){$fire++;}
	if($hour>=16 and $hour<=19){$gold++;}
	
	if($gold and $wood and $water and $fire and $soil){
		open(In,"gold.txt");
		while(<In>){
			chomp;
			push(@Name,$_);
		}
		close(In);
		open(In,"wood.txt");
		while(<In>){
			chomp;
			push(@Name,$_);
		}
		close(In);
		open(In,"water.txt");
		while(<In>){
			chomp;
			push(@Name,$_);
		}
		close(In);
		open(In,"fire.txt");
		while(<In>){
			chomp;
			push(@Name,$_);
		}
		close(In);
		open(In,"soil.txt");
		while(<In>){
			chomp;
			push(@Name,$_);
		}
		close(In);
	}else{
		if(!$gold){
			open(In,"gold.txt");
			while(<In>){
				chomp;
				push(@Name,$_);
			}
			close(In);
		}
		if(!$wood){
			open(In,"wood.txt");
			while(<In>){
				chomp;
				push(@Name,$_);
			}
			close(In);
		}
		if(!$water){
			open(In,"water.txt");
			while(<In>){
				chomp;
				push(@Name,$_);
			}
			close(In);
		}
		if(!$fire){
			open(In,"fire.txt");
			while(<In>){
				chomp;
				push(@Name,$_);
			}
			close(In);
		}
		if(!$soil){
			open(In,"soil.txt");
			while(<In>){
				chomp;
				push(@Name,$_);
			}
			close(In);
		}
	}
	open(In,"firstname.txt");
	while(<In>){
		chomp;
		push(@firstname,$_);
	}
	close(In);
	for($i=0;$i<5;$i++){
		$namelist[$i]=$firstname[int rand(@firstname)].$Name[int rand(@Name)];
		$namelist[$i]=decode('gb2312',$namelist[$i]);
	}
}

	
print "
<html>
	<head>
		<link rel='shortcut icon' href='icon.ico' type='image/x-icon'/>
		<title>在线中文起名系统</title>
			<style type='text/css'>

  body {background-image: url('/../09.jpg');
		background-repeat: no-repeat;
		background-attachment: fixed;
		background-size: cover;
}
h1,h3{
	text-align:center;
}

</style>

	</head>
	<body>
		<h1>下面是你得到的名字：</h1>
		<h3>$namelist[0]</h3> 
		<h3>$namelist[1]</h3>
		<h3>$namelist[2]</h3>
		<h3>$namelist[3]</h3>
		<h3>$namelist[4]</h3>
	</body>
</html>";