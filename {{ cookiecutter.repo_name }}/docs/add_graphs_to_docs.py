import os
import shutil
import click


@click.command()
@click.option('-s', '--source', type=click.Path(exists=True, file_okay=False))
@click.option('-d', '--docs', type=click.Path(exists=True, file_okay=False))
def main(source: str, docs: str):
    graphs_dir_name = 'graphs'
    graphs_dir_path = os.path.join(docs, graphs_dir_name)
    if os.path.exists(graphs_dir_path):
        shutil.rmtree(graphs_dir_path)
    os.makedirs(graphs_dir_path)

    for root, dirs, files in os.walk(source):
        graph_source_path = [
            dir_name
            for dir_name in os.path.split(root[len(source):])
            if dir_name and dir_name != os.path.sep
        ]
        docs_path = os.path.join(
            graphs_dir_path,
            *graph_source_path,
        )
        if not os.path.exists(docs_path):
            os.makedirs(docs_path)
        
        toctree_name = graph_source_path[-1] if graph_source_path else 'general'
        with open(os.path.join(docs_path, f'{toctree_name}_plots.rst'), 'w') as toctree:
            toctree.write('\n'.join([
                toctree_name,
                '===============',
                '',
                '.. toctree::',
                '   :glob:',
                '',
                f'   ./*',
                '',
            ]))  
        for filename in files:
            if filename.endswith('.html'):
                graph_name = os.path.splitext(filename)[0].lower()
                with open(os.path.join(docs_path, f'{graph_name}.rst'), 'w') as f:
                    f.write('\n'.join([
                        graph_name,
                        '===============',
                        '',
                        '.. raw:: html',
                        '',
                        f'    <iframe src="{os.path.join(os.path.abspath(source), *graph_source_path, filename)}" height="500px" width="100%"></iframe>',
                    ]))
    with open(os.path.join(docs, 'graph.rst'), 'w') as f:
        f.write('\n'.join([
            'Graph',
            '===============',
            '',
            '.. toctree::',
            '   :glob:',
            '',
            f'   {graphs_dir_name}/**_plots',
            '',
        ]))           


if __name__ == "__main__":
    main()
