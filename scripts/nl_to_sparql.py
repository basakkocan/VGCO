import sys
from prettytable import PrettyTable
import sparql_translator

def display_results(query_str: str, headers: list, rows: list):
    """Print the SPARQL query and format the results in a table."""
    print("\n" + "="*80)
    print(">>> GENERATED SPARQL QUERY:")
    print("="*80)
    print(query_str)
    print("="*80)
    
    if not rows:
        print("\nEmpty results. No matching records found in the ontology.")
        print("="*80 + "\n")
        return
        
    print(f"\n--- QUERY RESULTS (Count: {len(rows)}):")
    table = PrettyTable()
    table.field_names = headers
    # Left-align text columns
    table.align = "l"
    
    for row in rows:
        # Truncate long descriptions to keep table readable in terminal
        truncated_row = []
        for cell in row:
            cell_str = str(cell)
            if len(cell_str) > 50:
                truncated_row.append(cell_str[:47] + "...")
            else:
                truncated_row.append(cell_str)
        table.add_row(truncated_row)
        
    print(table)
    print("="*80 + "\n")

def run_interactive(graph):
    """Run an interactive console loop for translating questions."""
    print("\n" + "*"*80)
    print(" Video Game Catalog Ontology (VGCO) - Natural Language Query Interface")
    print("*"*80)
    print("Type your questions in English or Turkish.")
    print("Type 'exit' or 'quit' or press Ctrl+C to close the shell.")
    print("*"*80 + "\n")
    
    while True:
        try:
            question = input("Ask VGCO > ").strip()
            if not question:
                continue
            if question.lower() in ["exit", "quit", "q"]:
                print("Goodbye!")
                break
                
            print("Thinking...")
            sparql_query, headers, rows = sparql_translator.translate_and_query(question, graph)
            display_results(sparql_query, headers, rows)
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\n[ERROR] Error: {e}\n")

def main():
    # Load ontology graph first to avoid reloading it on every query in interactive mode
    print("Loading VGCO ontology graphs into memory...")
    try:
        graph = sparql_translator.load_ontology_graph()
        print(f"Ontology loaded successfully. Total triples: {len(graph)}")
    except Exception as e:
        print(f"[ERROR] Error loading ontology: {e}")
        sys.exit(1)
        
    # Check if a query was passed as command line arguments
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
        print(f"Question: {question}")
        print("Thinking...")
        try:
            sparql_query, headers, rows = sparql_translator.translate_and_query(question, graph)
            display_results(sparql_query, headers, rows)
        except Exception as e:
            print(f"[ERROR] Error: {e}")
            sys.exit(1)
    else:
        run_interactive(graph)

if __name__ == "__main__":
    main()
