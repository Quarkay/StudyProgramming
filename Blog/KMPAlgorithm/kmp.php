<?php
//Date: 2016.03
//Author: 一把杀猪刀 blog: www.mierhuo.com

$pat = 'abaabcac';
//'  ###01122312'

function get_nextArr($pat){
	$pat = ' '.$pat;
	$patLen = strlen($pat)-1;
	$nextArr = array(0=>$patLen,1=>0);
	$i = 1;
	$j = 0;

	while ($i < $patLen) {
		if($j == 0 || $pat[$i] == $pat[$j]){
			$i ++ ;
			$j ++ ;
			$nextArr[$i] = $j;
		}else{
			$j = $nextArr[$j];
		}
	}

	return $nextArr; 
}

print_r(get_nextArr($pat));