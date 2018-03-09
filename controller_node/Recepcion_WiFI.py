from wifi import Cell, Scheme
cell = Cell.all('wlp5s0');
var=0;
while (var!=len(cell)):
	print "Nombre de la red:",cell[var].signal,"y",cell[var].ssid,"dbm"
	var=var+1
	


