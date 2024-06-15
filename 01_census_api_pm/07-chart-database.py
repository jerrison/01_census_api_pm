from graphviz import Digraph

def create_er_diagram():
    dot = Digraph(comment='Entity Relationship Diagram')

    # Define nodes for tables
    dot.node('datasets', 'datasets\nuid (PK)\nid (FK)\nname\ndatacoverage\nmindate\nmaxdate')
    dot.node('data_categories', 'data_categories\nid (PK)\nname')

    # Define relationships
    dot.edge('datasets', 'data_categories', label='id (FK)')

    # Save the diagram as an image
    dot.render('er_diagram', format='png')

if __name__ == "__main__":
    create_er_diagram()
