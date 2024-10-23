import json
from datetime import datetime

# Function to generate SQL INSERT statements
def generate_sql_insert(participants):
    # Define the base SQL template
    sql_template = (
        "INSERT INTO `participants` "
        "(`show_id`, `name`, `dial_number`, `entry_date`, `evicted_date`, `image`, `full_image`, `created_at`, `updated_at`) "
        "VALUES ('{show_id}', '{name}', '{dial_number}', '{entry_date}', '{evicted_date}', '{image}', '{full_image}', '{created_at}', '{updated_at}');"
    )

    # Get the current date and time for created_at and updated_at
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Initialize list to collect SQL statements
    sql_statements = []

    # Process each participant
    for participant in participants:
        # Extract data
        show_id = '1'  # Assuming a constant value for this example
        name = participant.get('name', '')
        dial_number = participant.get('dial_number', '')
        entry_date = '2023-10-01'  # Placeholder value, adjust as needed
        evicted_date = participant.get('eliminated_date', '')
        image = participant.get('image', '')
        full_image = participant.get('full_image', '')
        created_at = now
        updated_at = now

        # Generate SQL statement
        sql_statement = sql_template.format(
            show_id=show_id,
            name=name,
            dial_number=dial_number,
            entry_date=entry_date,
            evicted_date=evicted_date,
            image=image,
            full_image=full_image,
            created_at=created_at,
            updated_at=updated_at
        )

        # Append to list
        sql_statements.append(sql_statement)

    # Return all SQL statements joined by newline
    return '\n'.join(sql_statements)

# Main function to read JSON from file and generate SQL
def main():
    input_file = 'shows/tamil_session_7.json'  # Replace with your JSON file path
    output_file = 'insert_statements.sql'  # File to save the SQL statements

    # Read JSON data from file
    with open(input_file, 'r') as f:
        data = json.load(f)

    # Generate SQL inserts
    sql_inserts = generate_sql_insert(data.get('participants', []))

    # Save SQL statements to file
    with open(output_file, 'w') as f:
        f.write(sql_inserts)

    print(f'SQL statements have been written to {output_file}')

# Run the main function
if __name__ == '__main__':
    main()