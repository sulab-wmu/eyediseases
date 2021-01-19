<!--
  - Copyright (c) 2018-2021 Beijing Ekitech Co., Ltd.
  - All rights reserved.
  -->

<template>
    <section class="section">
        <div class="container">
            <div class="content">
                <h1 class="title">1. Introduction</h1>
                <p>EyeDiseases is a omics database which integrates gene, mutation, RNA expression, Single-Cell RNAseq, methylation, chromatin accessibility and histone modification data. The database
                    provides three functions, ‘Genetics’, ‘Expression’, and ‘Epigenomics’, to help researchers visualize the relationships between eye disease and candidate genes. Data in this
                    database
                    were performed extended functional annotation, such as gene-disease networks, Gene Ontology, Pathway analysis and Co-expression. Therefore, EyeDiseases uniformed processing
                    pipelines
                    to create high-quality, consistent, and reproducible data. Our mission is to provide the scientific community with freely available information on eye disease-related gene, RNA
                    expression and epigenetic regulation.
                </p>

                <h1 class="title">2. Data Collection</h1>
                <p>We performed a comprehensive search in OMIM, GWAS catalog and PubMed for gene and variants related with eye diseases, and a total of genes, variants, studies were collected.
                    Microarray,
                    bulk-cell RNAseq, single-cell RNAseq and epigenomic data were collected from GEO (Gene Expression Omnibus).</p>
                <h1>3. Data Processing Pipelines</h1>
                <h2 class="subtitle">RNA-seq</h2>
                <h4>Step 1: Building the STAR index.*</h4>
                <div class="cnblogs_code">
                    <pre>{{ code1 }}</pre>
                </div>

                <h4>Step 2: Alignment</h4>
                <div class="cnblogs_code">
                    <pre>{{ code2 }}</pre>
                </div>

                <h4>Step 3: Count</h4>
                <div class="cnblogs_code">
                    <pre>{{ code3 }}</pre>
                </div>

                <h2 class="subtitle">Microarray</h2>
                <ol>
                    <li>Illumina: log2 transformed and quantile normalized using the lumi package in R.</li>
                    <li>Affymetrix: background correction, log2 transformation, quantile normalization, and probe summarization using the oligo package in R.</li>
                    <li>Agilent: read.maimages, backgroundCorrect, normalizeWithinArrays, normalizeBetweenArrays, getEAWP functions using the limma package in R.</li>
                </ol>

                <h2 class="subtitle">Single-cell pipeline</h2>
                <h4>Step 1: read</h4>
                <p>The `Read10X` function reads in the output of the [cellranger] pipeline from 10X, returning a unique molecular identified (UMI) count matrix. The values in this matrix represent the
                    number of molecules for each feature (i.e. gene; row) that are detected in each cell (column).</p>

                <div class="cnblogs_code">
                    <pre>{{ code4 }}</pre>
                </div>
                <h4>Step 2: QC and selecting cells</h4>
                <div class="cnblogs_code">
                    <pre>{{ code5 }}</pre>
                </div>
                <h4>Step 3: data normalization and scale</h4>
                <p>we employ a global-scaling normalization method “LogNormalize” that normalizes the feature expression measurements. For each cell by the total expression, multiplies this by a scale
                    factor (10,000 by default) and log-transforms the result. We then apply a linear transformation ('scaling') that is a standard pre-processing step prior to dimensional reduction
                    techniques like PCA using `ScaleData` function.</p>
                <div class="cnblogs_code">
                    <pre>{{ code6 }}</pre>
                </div>

                <h4>Step 4: feature selection and PCA</h4>
                <div class="cnblogs_code">
                    <pre>{{ code7 }}</pre>
                </div>

                <h4>Step 5: Determine the 'dimensionality' of the dataset</h4>
                <div class="cnblogs_code">
                    <pre>{{ code8 }}</pre>
                </div>

                <h4>Step 6: Cluster the cells</h4>
                <div class="cnblogs_code">
                    <pre>{{ code9 }}</pre>
                </div>

                <h4>Step 7: Finding differentially expressed features</h4>
                <p>`FindAllMarkers` function automates this process for all clusters, and seurat can help to find markers that define clusters via differential expression. </p>
                <div class="cnblogs_code">
                    <pre>{{ code10 }}</pre>
                </div>

                <h2 class="subtitle">ChIP-seq and ATAC-seq pipelines</h2>
                <h4>Step 1: Bowtie2 Alignment</h4>
                <div class="cnblogs_code">
                    <pre>{{ code11 }}</pre>
                </div>

                <h4>Step 2: sam to bam</h4>
                <div class="cnblogs_code">
                    <pre>{{ code12 }}</pre>
                </div>

                <h4>Step 3: MarkDuplicates</h4>
                <div class="cnblogs_code">
                    <pre>{{ code13 }}</pre>
                </div>

                <h4>Step 4: bam to bigwig</h4>
                <div class="cnblogs_code">
                    <pre>{{ code13 }}</pre>
                </div>

                <h2 class="subtitle">DNA methylation pipeline</h2>
                <h4>Step 1: build index</h4>
                <div class="cnblogs_code">
                    <pre>{{ code14 }}</pre>
                </div>

                <h4>Step 2: bismark_mapping</h4>
                <div class="cnblogs_code">
                    <pre>{{ code15 }}</pre>
                </div>

                <h4>Step 3: extract methylation level</h4>
                <div class="cnblogs_code">
                    <pre>{{ code16 }}</pre>
                </div>

                <h4>Step 4: create bigwig</h4>
                <div class="cnblogs_code">
                    <pre>{{ code17 }}</pre>
                </div>

                <h1 class="title">4. Data analysis</h1>
                <h4>(1) Gene-disease network</h4>
                <p>To facilitate the exploration of the exceptional genetic heterogeneity of EyeDiseases, gene-disease network, implemented by SVG, was completed to graphically and vividly show
                    intrinsic
                    relations between EyeDiseases genes and EyeDiseases. </p>
                <h4>(2) Gene Ontology and pathway analysis</h4>
                <p>Gene Ontology annotation, including such four parts as biological process, cellular component, molecular function and KEGG, was performed by DAVID. Each part contains the GO term
                    accession, GO term name, Ratio of enrichment, P-Value, Adjusted P-value and Genes related. Enriched pathway information also was accessed through DAVID. </p>
                <h4>(3) Co-expression</h4>
                <p>To place results from individual genes within systems-level network architecture, we performed Weighted Gene Co-Expression Network Analysis (WGCNA). Individual expression datasets
                    were
                    combined together using the genes present across all studies. ComBat was used to mitigate batch effects. Network analysis was performed with the WGCNA package using signed
                    network</p>
            </div>
        </div>
    </section>
</template>

<script>
    export default {
        data() {
            return {
                code1: 'STAR --runMode genomeGenerate \\ \n --genomeDir <star_index_path> \\ \n --genomeFastaFiles <reference> \\ \n --sjdbOverhang 150 \\ \n --sjdbGTFfile < Homo_sapiens.GRCh38.95.gtf >\
               \n --runThreadN 8',
                code2: 'STAR --runMode alignReads \\ \n --runThreadN 16 \\ \n --genomeDir <star_index_path> \\ \n --readFilesIn <fastq_left_1>,<fastq_right_1> \\ \n --twopassMode Basic \\ \n --sjdbOverhang 149 \\ \n --outFilterMultimapNmax 20 \\ \n --alignSJoverhangMin 8 \\ \n --alignSJDBoverhangMin 1 \\ \n --outFilterMismatchNmax 999 \\ \n --alignIntronMin 20 \\ \n --alignIntronMax 1000000 \\ \n --alignMatesGapMax 1000000 \\ \n --sjdbScore 2 \\ \n --outFilterType BySJout \\ \n --outFilterScoreMinOverLread 0.33 \\ \n --outFilterMatchNminOverLread 0.33 \\ \n --limitSjdbInsertNsj 1200000 \\ \n --readFilesCommand zcat \\ \n --outFileNamePrefix <sample_id> \\ \n --outSAMstrandField intronMotif \\ \n --outFilterIntronMotifs None \\ \n --alignSoftClipAtReferenceEnds Yes \\ \n --quantMode TranscriptomeSAM GeneCounts \\ \n --outSAMtype BAM SortedByCoordinate \\ \n --outSAMunmapped Within \\ \n --genomeLoad NoSharedMemory \\ \n --chimSegmentMin 15 \\ \n --chimJunctionOverhangMin 15 \\ \n --chimSegmentReadGapMax 3 \\ \n --chimOutType Junctions WithinBAM \\ \n --alignSJstitchMismatchNmax 5 -1 5 5 \\ \n --chimOutJunctionFormat 1 \\ \n --outSAMattributes NH HI AS nM NM ch XS MD \\ \n --outSAMattrRGline ID:rg1 SM:sm1',
                code3: 'samtools view -F 4 <bam_file> | \ htseq-count -i gene_id \\ \n -r pos \\ \n -s reverse \\ \n - Homo_sapiens.GRCh38.95.gtf \\ \n > <output.count>',
                code4: 'pbmc <- Read10X(data.dir = "./") \npbmc <- CreateSeuratObject(counts = pbmc)',
                code5: 'pbmc <- subset(x = pbmc, subset = nCount_RNA > * & nFeature_RNA > * & nFeature_RNA < * & percent.mt < *)',
                code6: "pbmc <- NormalizeData(object = pbmc, normalization.method = 'LogNormalize', scale.factor = 10000) \npbmc <- ScaleData(object = pbmc, features = all.genes, vars.to.regress = c('nCount_RNA', 'percent.mt’))",
                code7: "pbmc <- FindVariableFeatures(object = pbmc, selection.method = 'vst', nfeatures = 2000) \npbmc <- RunPCA(object = pbmc, features = VariableFeatures(object = pbmc))",
                code8:
                    'pbmc <- JackStraw(object = pbmc, num.replicate = 100) \npbmc <- ScoreJackStraw(object = pbmc, dims = 1:20) \nJackStrawPlot(object = pbmc, dims = 1:15) \nElbowPlot(object = pbmc)',
                code9: 'pbmc <- FindNeighbors(object = pbmc, dims = 1:20) \npbmc <- FindClusters(object = pbmc, resolution = 0.8) \npbmc <- RunTSNE(object = pbmc, dims = 1:20)',
                code10: 'pbmc.markers <- FindAllMarkers(pbmc, only.pos = TRUE, min.pct = 0.25, logfc.threshold = 0.25)',
                code11: 'bowtie2 -p 4 \\ \n --local -x <reference> \\ \n -U <fastq_file> \\ \n -S <output.sam> \n \nbowtie2 -p 4 \\ \n --local -x <reference> \\ \n -1 <fastq_left_1> \\ \n -2 <fastq_right_1> \\ \n -S <output.sam>',
                code12: 'samtools view –h \\ \n -S \\ \n -b \\ \n -o <output.bam> \n <input.sam> \n \n \nsambamba sort -t 4 \\ \n -o <output.sorted.bam> \n <input.bam> \n \n \nsambamba view –h \\ \n -t 4 \\ \n -f bam \\ \n -F "[XS] == null and not unmapped  and not duplicate” \\ \n -o <input.sorted.bam> \\ \n > <output.sorted.unique.bam>',
                code13: 'java -jar picard.jar MarkDuplicate \\ \n I=<input.sorted.unique.bam> \\ \n O=<output.sorted.unique.marked.bam> \\ \n M=<output.markeddupmetrics> \\ \n REMOVE_DUPLICATES=true \\ \n ASSUME_SORTED=true',
                code14: 'samtools index <output.sorted.unique.marked.bam> \nbamCoverage –b <output.sorted.unique.marked.bam> \\ \n --normalizeUsing RPKM \\ \n --ignoreForNormalization chrX chrY chrMT \\ \n --binSize 50 \\ \n -p 5 \\ \n --ignoreDuplicates \\ \n --skipNonCoveredRegions \\ \n --outFileFormat bigwig \\ \n -o <output.bw>',
                code15: 'bismark_genome_preparation --path_to_bowtie /usr/bin/bowtie2/ \\ \n --verbose \\ \n --bowtie2 \\ \n <bismark_index_path>',
                code16: 'bismark < bismark_index_path > --parallel 4 \\ \n-1 <fastq_left_1> \\ \n-2 <fastq_right_1> \\ \n--path_to_bowtie < path_to_bowtie> \\ \n-o <output_dir> \\ \n--temp_dir <temp_dir>',
                code17: 'bismark_methylation_extractor –s \\ \n --comprehensive \\ \n --bedGraph \\ \n --counts <input.bam> \\ \n -o <output_dir> \\ \n --parallel 5 \\ \n --cytosine_report \\ \n --genome_folder bismark_index_path ',
                code18: 'towig -i <output.bismark.cov.gz> \\ \n -m_u 5,6 \\ \n -n <sample_id> \\ \n -o < output_dir > \\ \n --depth 5 \\ \n --merge \\ \n --genome <reference> \n wigToBigWig <output.wig> <chrom.sizes> <output.bw>',
            }
        }
    }
</script>

<style scoped>
ul li {
    list-style: disc;
    margin-left: 30px;
}

.cnblogs_code {
    background-color: #f5f5f5;
    font-family: monospace !important;
    border: 1px solid #ccc;
    padding: 5px;
    margin-bottom: 1em;
}
</style>
