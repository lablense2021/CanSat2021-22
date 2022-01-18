
Param(
    [Parameter(Mandatory=$True)]
    [string]$fn 
)

[string] $loc = Get-Location 


[string] $f = $loc + "\" + $fn

scp $f pi@192.168.3.132:software

$c = "sudo python3 software/" + $fn 

ssh 192.168.0.10 -p 22 -l pi -t $c 



