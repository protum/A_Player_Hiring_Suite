import { useState } from 'react';
import { systemApi } from '../services/api';
import { ArrowDownTrayIcon, ArrowUpTrayIcon } from '@heroicons/react/24/outline';

export default function Settings() {
  const [exporting, setExporting] = useState(false);
  const [importing, setImporting] = useState(false);

  const handleExportBackup = async (format: string) => {
    setExporting(true);
    try {
      const response = await systemApi.exportBackup(format);
      const blob = new Blob([response.data], {
        type: format === 'sqlite' ? 'application/octet-stream' : 'application/json',
      });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `backup_${new Date().toISOString().split('T')[0]}.${format === 'sqlite' ? 'db' : 'json'}`;
      a.click();
    } catch (error) {
      console.error('Error exporting backup:', error);
      alert('Error exporting backup');
    } finally {
      setExporting(false);
    }
  };

  const handleImportBackup = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setImporting(true);
    try {
      await systemApi.importBackup(file);
      alert('Backup imported successfully. Please refresh the page.');
    } catch (error) {
      console.error('Error importing backup:', error);
      alert('Error importing backup');
    } finally {
      setImporting(false);
    }
  };

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Settings</h1>
        <p className="mt-2 text-gray-600">
          Manage application settings and data backups
        </p>
      </div>

      <div className="space-y-6">
        <div className="card">
          <h2 className="text-lg font-semibold mb-4">Data Backup & Export</h2>
          <p className="text-sm text-gray-600 mb-4">
            Export or import your entire database for backup or migration purposes.
          </p>

          <div className="space-y-4">
            <div>
              <h3 className="text-sm font-medium text-gray-700 mb-2">Export Database</h3>
              <div className="flex gap-2">
                <button
                  onClick={() => handleExportBackup('sqlite')}
                  disabled={exporting}
                  className="btn btn-primary flex items-center gap-2"
                >
                  <ArrowDownTrayIcon className="h-4 w-4" />
                  {exporting ? 'Exporting...' : 'Export SQLite Database'}
                </button>
                <button
                  onClick={() => handleExportBackup('json')}
                  disabled={exporting}
                  className="btn btn-secondary flex items-center gap-2"
                >
                  <ArrowDownTrayIcon className="h-4 w-4" />
                  {exporting ? 'Exporting...' : 'Export JSON'}
                </button>
              </div>
            </div>

            <div>
              <h3 className="text-sm font-medium text-gray-700 mb-2">Import Database</h3>
              <div className="flex items-center gap-2">
                <label className="btn btn-secondary flex items-center gap-2 cursor-pointer">
                  <ArrowUpTrayIcon className="h-4 w-4" />
                  {importing ? 'Importing...' : 'Import Backup'}
                  <input
                    type="file"
                    accept=".db,.json"
                    onChange={handleImportBackup}
                    disabled={importing}
                    className="hidden"
                  />
                </label>
                <p className="text-sm text-gray-500">
                  Accepts .db or .json files
                </p>
              </div>
              <p className="text-xs text-orange-600 mt-2">
                Warning: Importing will overwrite existing data. Make sure to export a backup first.
              </p>
            </div>
          </div>
        </div>

        <div className="card">
          <h2 className="text-lg font-semibold mb-4">About</h2>
          <div className="space-y-3 text-sm">
            <div>
              <span className="font-medium text-gray-700">Application:</span>{' '}
              <span className="text-gray-600">A-Player Hiring Suite</span>
            </div>
            <div>
              <span className="font-medium text-gray-700">Version:</span>{' '}
              <span className="text-gray-600">1.0.0</span>
            </div>
            <div>
              <span className="font-medium text-gray-700">Mode:</span>{' '}
              <span className="text-gray-600">Local (Offline)</span>
            </div>
            <div>
              <span className="font-medium text-gray-700">Data Storage:</span>{' '}
              <span className="text-gray-600">SQLite (Local)</span>
            </div>
          </div>
        </div>

        <div className="card bg-blue-50 border-blue-200">
          <h2 className="text-lg font-semibold mb-2">Evidence-Based Methodologies</h2>
          <p className="text-sm text-gray-700 mb-3">
            This application implements hiring and leadership assessment frameworks from:
          </p>
          <ul className="space-y-2 text-sm text-gray-700">
            <li>• <strong>Who: The A Method for Hiring</strong> - Geoff Smart & Randy Street</li>
            <li>• <strong>Topgrading</strong> - Bradford D. Smart</li>
            <li>• <strong>Foolproof Hiring</strong> - Karen Kocher</li>
            <li>• <strong>The CEO Next Door</strong> - Elena L. Botelho & Kim R. Powell</li>
            <li>• <strong>Power Score</strong> - Leadership assessment methodology</li>
          </ul>
        </div>
      </div>
    </div>
  );
}
