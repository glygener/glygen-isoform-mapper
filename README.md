The isoform-mapper tool is used to map protein sequence position on UniProtKB isoform sequences to corrsponding canonical 
siform sequence by performing global pairwise alignment.

### Step-1: pull image from docker hub
```
docker pull glygen/isoform-mapper:1.0.0
```

### Step-2: set up your data folder
Choose path to your data directory (for example DATA_DIR="/path/to/data/directory/") and run the following commands to create subdirectories

```
$ mkdir -p $DATA_DIR/db
$ mkdir -p $DATA_DIR/input_examples
$ mkdir -p $DATA_DIR/logs
$ mkdir -p $DATA_DIR/output
```

### Step-3: place fasta files under $DATA_DIR/db
You can use the following commands to download isoform sequences for different proteomes 
```
$ wget https://data.glygen.org/ln2data/releases/data/current/reviewed/human_protein_allsequences.fasta -O $DATA_DIR/db/human_protein_allsequences.fasta
$ wget https://data.glygen.org/ln2data/releases/data/current/reviewed/mouse_protein_allsequences.fasta -O $DATA_DIR/db/human_protein_allsequences.fasta
$ wget https://data.glygen.org/ln2data/releases/data/current/reviewed/rat_protein_allsequences.fasta -O $DATA_DIR/db/rat_protein_allsequences.fasta
```
If you want to use isoform sequence files for proteomes that are not available at https://data.glygen.org, you can do so as long as the fasta file is organized to include UniProtKB accessions for both the isoform (O60353-2) and corresponding canonical (O60353-1) sequences as shown below.

```
>sp|O60353-2|FZD6_HUMAN Isoform 2 of Frizzled-6 OS=Homo sapiens OX=9606 GN=FZD6 PE=1 SV=2 CANONICAL=O60353-1
MKMAYNMTFFPNLMGHYDQSIAAVEMEHFLPLANLECSPNIETFLCKAFVPTCIEQIHVV
PPCRKLCEKVYSDCKKLIDTFGIRWPEELECDRLQYCDETVPVTFDPHTEFLGPQKKTEQ
VQRDIGFWCPRHLKTSGGQGYKFLGIDQCAPPCPNMYFKSDELEFAKSFIGTVSIFCLCA
TLFTFLTFLIDVRRFRYPERPIIYYSVCYSIVSLMYFIGFLLGDSTACNKADEKLELGDT
VVLGSQNKACTVLFMLLYFFTMAGTVWWVILTITWFLAAGRKWSCEAIEQKAVWFHAVAW
GTPGFLTVMLLAMNKVEGDNISGVCFVGLYDLDASRYFVLLPLCLCVFVGLSLLLAGIIS
LNHVRQVIQHDGRNQEKLKKFMIRIGVFSGLYLVPLVTLLGCYVYEQVNRITWEITWVSD
HCRQYHIPCPYQAKAKARPELALFMIKYLMTLIVGISAVFWVGSKKTCTEWAGFFKRNRK
RDPISESRRVLQESCEFFLKHNSKVKHKKKHYKPSSHKLKVISKSMGTSTGATANHGTSA
VAITSHDYLGQETLTEIQTSPETSMREVKADGASTPRLREQDCGEPASPAASISRLSGEQ
VDGKGQAGSVSESARSEGRISPKSDITDTGLAQSNNLQVPSSSEPSSLKGSTSLLVHPVS
GVRKEQGGGCHSDT


```

### Step-4: create example input file and place fasta files under $DATA_DIR/input_examples/
Create a CSV file containing the following lines and save it as $DATA_DIR/input_examples/input.1.csv
```
isoform_ac,amino_acid_pos,amino_acid
A6NJB7-2,3,T
A6NJB7-2,8,S
P08697-2,36,T
P08697-2,37,S
P19827-2,514,S
P19827-2,516,N
P19827-2,517,T
```

### Step-5: run isoform mapper
Use the following command to test the isoform mapper
```
$ docker run --rm -v $DATA_DIR:/data glygen/isoform-mapper:1.0.0 python run-isoform-mapper.py  -i /data/input_examples/input.1.csv -o /data/output/output.1.tsv
```

### Step-6: check output file and (logs)
Use the following command to test the isoform mapper
```
$ ls -ltr $DATA_DIR/logs/
$ cat $DATA_DIR/output/output.1.tsv
```
Successful run of the above command will generate the following $DATA_DIR/output/output.1.tsv file

```
uniprotkb_isoform_ac	aa_pos_isoform	aa_isoform_user	aa_isoform_actual	glygen_canonical_ac	aa_pos_canonical	aa_canonical	warning	error
A6NJB7-2	3	T	T	A6NJB7-1	3	T		
A6NJB7-2	8	S	S	A6NJB7-1	8	S		
P08697-2	36	T	T	P08697-1	36	T		
P08697-2	37	S	S	P08697-1	37	S		
P19827-2	514	S	S	P19827-1	656	S		
P19827-2	516	N	N	P19827-1	658	N		
P19827-2	517	T	T	P19827-1	659	T
```









