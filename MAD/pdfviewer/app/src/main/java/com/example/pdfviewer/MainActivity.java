package com.example.pdfviewer;

import android.net.Uri;
import android.os.Build;
import android.os.Bundle;

import androidx.activity.EdgeToEdge;
import androidx.activity.result.ActivityResultLauncher;
import androidx.activity.result.contract.ActivityResultContracts;
import androidx.annotation.RequiresExtension;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;
import androidx.fragment.app.FragmentManager;
import androidx.fragment.app.FragmentTransaction;
import androidx.pdf.viewer.fragment.PdfViewerFragment;

import com.google.android.material.button.MaterialButton;

@RequiresExtension(extension = Build.VERSION_CODES.S, version = 13)
public class MainActivity extends AppCompatActivity {

    private static final String PDF_VIEWER_FRAGMENT_TAG = "pdf_viewer_fragment_tag";
    private PdfViewerFragment pdfViewerFragment;

    private final ActivityResultLauncher<String> filePicker =
            registerForActivityResult(new ActivityResultContracts.GetContent(), uri -> {
                if (uri != null) {
                    showPdf(uri);
                }
            });

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_main);
        
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });

        MaterialButton launchButton = findViewById(R.id.launch_button);

        launchButton.setOnClickListener(v -> filePicker.launch("application/pdf"));
        


        pdfViewerFragment = (PdfViewerFragment) getSupportFragmentManager().findFragmentByTag(PDF_VIEWER_FRAGMENT_TAG);
    }

    private void showPdf(Uri uri) {
        if (pdfViewerFragment == null) {
            pdfViewerFragment = new PdfViewerFragment();
            FragmentManager fragmentManager = getSupportFragmentManager();
            FragmentTransaction transaction = fragmentManager.beginTransaction();
            transaction.replace(R.id.fragment_container_view, pdfViewerFragment, PDF_VIEWER_FRAGMENT_TAG);
            transaction.commitAllowingStateLoss();
            fragmentManager.executePendingTransactions();
        }
        pdfViewerFragment.setDocumentUri(uri);
    }
}
