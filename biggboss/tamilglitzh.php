<?php

// Function to fetch content from a URL
function getUrlContents($url) {
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
    $output = curl_exec($ch);
    curl_close($ch);
    return $output;
}

// Function to extract the View Results link, and click it
function getVoteResultsLink($htmlContent) {
    // Create DOMDocument and load HTML content
    $dom = new DOMDocument();
    @$dom->loadHTML($htmlContent); // Suppress warnings for malformed HTML

    // Create DOMXPath to navigate the HTML
    $xpath = new DOMXPath($dom);

    // Find the 'TamilGlitz | View Results' link
    $viewResultsLink = $xpath->query("//a[contains(text(),'View Results')]");

    if ($viewResultsLink->length > 0) {
        $href = $viewResultsLink->item(0)->getAttribute('href');
        return $href;  // Return the href of the 'View Results' link
    }

    return null;
}

// Function to extract the results after visiting the results page
function extractResults($htmlContent) {
    // Create DOMDocument and load HTML content
    $dom = new DOMDocument();
    @$dom->loadHTML($htmlContent);

    // Create DOMXPath to navigate the HTML
    $xpath = new DOMXPath($dom);

    // Find all labels with class 'pds-feedback-label'
    $labels = $xpath->query("//label[contains(@class, 'pds-feedback-label')]");

    $results = [];

    foreach ($labels as $label) {
        // Extract the title from the 'pds-answer-text' class
        $titleNode = $xpath->query(".//span[contains(@class, 'pds-answer-text')]", $label);
        $title = $titleNode->length > 0 ? trim($titleNode->item(0)->textContent) : '';

        // Extract the result from 'pds-feedback-result' class
        $resultNode = $xpath->query(".//span[contains(@class, 'pds-feedback-result')]", $label);
        $result = $resultNode->length > 0 ? trim($resultNode->item(0)->textContent) : '';

        // Store the result in an array
        $results[] = [
            'title' => $title,
            'result' => $result
        ];
    }

    return $results;
}

// Main code
$mainPageUrl = "https://tamilglitz.in/bigg-boss-tamil-vote/";

// Fetch the content of the main page
$mainPageHtml = getUrlContents($mainPageUrl);

// Get the View Results link
$resultsLink = getVoteResultsLink($mainPageHtml);

if ($resultsLink) {
    // Fetch the content of the results page
    $resultsPageHtml = getUrlContents($resultsLink);

    // Extract and display the vote results
    $results = extractResults($resultsPageHtml);

    // Output the extracted results
    foreach ($results as $result) {
        echo "Title: " . $result['title'] . "\n";
        echo "Result: " . $result['result'] . "\n\n";
    }
} else {
    echo "View Results link not found.";
}

?>
