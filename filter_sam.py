#Filter sam


import click

@click.command()
@click.option('--sam','-s', required=True, help='Sam file to be filtered')
@click.option('--filter-list','-f','filter', required=True, help='List of ncbi sequence ids to remove from sam.')
@click.option('--output','-o', default="filtered.sam", help='Output sam file.')

def filter_sam(sam,filter, output):
    #Get set of ncbi_ids for filtering
    filter_set = set( line.strip() for line in open(filter) )
    #Filter
    with open(sam, 'r') as openin, open(output, 'w') as openout:
        for line in openin:
            if line.split('\t')[2] not in filter_set:
                openout.write(line)


if __name__ == "__main__":
    filter_sam()
